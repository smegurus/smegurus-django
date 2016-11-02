import django_filters
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string    # HTML to TXT
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives    # Emailer
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
from foundation_tenant.models.base.message import Message
from smegurus.settings import env_var
from smegurus import constants


class SendEmailViewMixin(object):
    def get_web_view(self, message):
        url = 'https://' if self.request.is_secure() else 'http://'
        url += self.request.tenant.schema_name + "."
        url += get_current_site(self.request).domain
        url += reverse('foundation_email_message', args=[message.id,])
        return url

    def get_message_url(self, message):
        url = 'https://' if self.request.is_secure() else 'http://'
        url += self.request.tenant.schema_name + "."
        url += get_current_site(self.request).domain
        url += reverse('tenant_conversation', args=[message.sender.id,])
        url = url.replace("None","en")
        return url

    def send_notification(self, message):
        # Generate the data.
        subject = "New Message"
        param = {
            'user': self.request.user,
            'message': message,
            'url': self.get_message_url(message),
            'web_view_url': self.get_web_view(message),
        }

        # Plug-in the data into our templates and render the data.
        text_content = render_to_string('tenant_message/message.txt', param)
        html_content = render_to_string('tenant_message/message.html', param)

        # Generate our address.
        from_email = env_var('DEFAULT_FROM_EMAIL')
        to = [message.recipient.owner.email,]

        # Send the email.
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()


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
            self.send_notification(instance)

    def perform_destroy(self, instance):
        """Override the deletion function to archive the message instead of deleting it."""
        if self.request.user.is_authenticated():
            instance.participants.remove(self.request.tenant_me)
            instance.save()
