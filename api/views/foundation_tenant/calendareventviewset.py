import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrIsAnEmployee
from api.serializers.foundation_tenant  import CalendarEventSerializer
from foundation_tenant.models.calendarevent import CalendarEvent
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.tag import Tag
from smegurus import constants


class CalendarEventFilter(django_filters.FilterSet):
    class Meta:
        model = CalendarEvent
        fields = ['name', 'description', 'type_of', 'colour', 'start', 'finish', 'owner', 'tags', 'pending', 'attendees', 'absentees',]


class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrIsAnEmployee, )
    filter_class = CalendarEventFilter

    def perform_create(self, serializer):
        """Override the create command to add additional computations."""
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
