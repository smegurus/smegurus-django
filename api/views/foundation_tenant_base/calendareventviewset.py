import django_filters
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string    # HTML to TXT
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives    # Emailer
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import detail_route
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrIsAnEmployee
from api.serializers.foundation_tenant_base  import CalendarEventSerializer
from api.serializers.misc  import IntegerSerializer
from foundation_tenant.models.base.calendarevent import CalendarEvent
from foundation_tenant.models.base.me import TenantMe
from foundation_tenant.models.base.tag import Tag
from smegurus.settings import env_var
from smegurus import constants


class SendEmailViewMixin(object):
    def get_web_view(self, calendar_event): #TODO: REMOVE
        url = 'https://' if self.request.is_secure() else 'http://'
        url += self.request.tenant.schema_name + "."
        url += get_current_site(self.request).domain
        url += reverse('foundation_email_calendar_pending_event', args=[calendar_event.id,])
        return url

    def get_calendar_event_url(self, calendar_event): #TODO: REMOVE
        """Function will return the URL to the calendar_event page through the sub-domain of the organization."""
        url = 'https://' if self.request.is_secure() else 'http://'
        url += self.request.tenant.schema_name + "."
        url += get_current_site(self.request).domain
        url += reverse('foundation_email_calendar_pending_event', args=[calendar_event.id,])
        url = url.replace("None","en")
        return url

    def send_notification(self, calendar_event):
        # Iterate through all the participants in the CalendarEvent and get their
        # email only if they request email notification for taks.
        contact_list = []
        for me in calendar_event.pending.all():
            if me.notify_when_task_had_an_interaction:
                contact_list.append(me.owner.email)

        # Generate the data.
        subject = "Pending Event #" + str(calendar_event.id)
        param = {
            'user': self.request.user,
            'calendar_event': calendar_event,
            'url': self.get_calendar_event_url(calendar_event), #TODO: Replace w/ resolve_full_url_with_subdmain
            'web_view_url': self.get_web_view(calendar_event), #TODO: Replace w/ resolve_full_url_with_subdmain
        }

        # Plug-in the data into our templates and render the data.
        text_content = render_to_string('tenant_calendar/pending_invite.html', param)
        html_content = render_to_string('tenant_calendar/pending_invite.html', param)

        # Generate our address.
        from_email = env_var('DEFAULT_FROM_EMAIL')
        to = contact_list

        # Send the email.
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class CalendarEventFilter(django_filters.FilterSet):
    class Meta:
        model = CalendarEvent
        fields = ['name', 'description', 'type_of', 'colour', 'start', 'finish', 'owner', 'tags', 'pending', 'attendees', 'absentees',]


class CalendarEventViewSet(SendEmailViewMixin, viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrIsAnEmployee, )
    filter_class = CalendarEventFilter

    def perform_create(self, serializer):
        """Override the create function to add additional computations."""
        # Include the owner attribute directly, rather than from request data.
        calendar_event = serializer.save(
            owner=self.request.user,
        )

        # If this event is by group invite, then take the groups and
        # assign the Users from each group into this event.
        if calendar_event.type_of == constants.CALENDAR_EVENT_BY_TAG_TYPE:
            for tag in calendar_event.tags.all():
                me = TenantMe.objects.get(tags__id=tag.id)
                calendar_event.pending.add(me)

        self.send_notification(calendar_event)  # Send notification to all users.

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def attending(self, request, pk=None):
        """Will set the current authenticated User to be attending this event."""
        try:
            calendar_event = self.get_object()
            calendar_event.pending.remove(request.tenant_me)
            calendar_event.absentees.remove(request.tenant_me)
            calendar_event.attendees.add(request.tenant_me)
            return response.Response(status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def abstaining(self, request, pk=None):
        """Will set the authenticated User to be abstaining from this event."""
        try:
            calendar_event = self.get_object()
            calendar_event.pending.remove(request.tenant_me)
            calendar_event.attendees.remove(request.tenant_me)
            calendar_event.absentees.add(request.tenant_me)
            return response.Response(status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
