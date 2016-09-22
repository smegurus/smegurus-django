import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import detail_route
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrIsAnEmployee
from api.serializers.foundation_tenant  import CalendarEventSerializer
from api.serializers.misc  import IntegerSerializer
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
