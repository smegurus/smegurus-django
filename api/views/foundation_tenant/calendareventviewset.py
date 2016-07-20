import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import ManagementOrAuthenticatedReadOnlyPermission
from api.serializers.foundation_tenant  import CalendarEventSerializer
from foundation_tenant.models.calendarevent import CalendarEvent


class CalendarEventFilter(django_filters.FilterSet):
    class Meta:
        model = CalendarEvent
        fields = ['name', 'start', 'finish', 'owner',]


class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, ManagementOrAuthenticatedReadOnlyPermission, )
    filter_class = CalendarEventFilter
