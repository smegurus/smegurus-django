import django_filters
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import detail_route
from api.permissions import IsMessageObjectPermission
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant import MessageSerializer
from foundation_tenant.models.message import Message
from smegurus.settings import env_var
from smegurus import constants


class SendEmailViewMixin(object):
    def login_url(self, schema_name):
        """Function will return the URL to the task page through the sub-domain of the organization."""
        url = 'https://' if self.request.is_secure() else 'http://'
        url += schema_name + "."
        url += get_current_site(self.request).domain
        url += reverse('foundation_auth_user_login')
        url = url.replace("None","en")
        return url

    def send_notification(self, schema_name, message):
        # Generate our email body text.
        url = self.login_url(schema_name)
        subject_text = 'New Message'
        html_text = _('%(sender_name)s sent you a message:\n\n \"%(sender_text)s\" \n\nLogin here to reply. %(url)s') % {
            'sender_name': message.sender.name,
            'sender_text': message.description,
            'url': str(url)
        }

        # Send the email.
        send_mail(
            subject_text,
            html_text,
            env_var('DEFAULT_FROM_EMAIL'),
            [message.recipient.owner.email],
            fail_silently=False
        )


class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = ['created', 'last_modified', 'owner', 'name', 'alternate_name',
                  'description', 'url', 'sender', 'recipient', 'participants',]


class MessageViewSet(SendEmailViewMixin, viewsets.ModelViewSet):
    queryset = Message.objects.filter()
    serializer_class = MessageSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsMessageObjectPermission)
    filter_class = MessageFilter

    def perform_create(self, serializer):
        """Add owner to this model when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(
            owner=self.request.user,
            sender=self.request.tenant_me,
        )

        # Add the sender and recipient to the participants in this conversation.
        # participants
        instance.participants.add(instance.sender, instance.recipient)
        instance.save()

        # Send an email notification to the recipient only if the User
        # specified that they would like to receive new message notifications.
        if instance.recipient.notify_when_new_messages:
            self.send_notification(self.request.tenant.schema_name, instance)

    def perform_destroy(self, instance):
        """Override the deletion function to archive the message instead of deleting it."""
        if self.request.user.is_authenticated():
            instance.participants.remove(self.request.tenant_me)
            instance.save()
