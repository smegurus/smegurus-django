import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import EmployeePermission
from api.serializers.foundation_tenant import EntrepreneurNoteSerializer
from foundation_tenant.models.entrepreneurnote import EntrepreneurNote


class EntrepreneurNoteFilter(django_filters.FilterSet):
    class Meta:
        model = EntrepreneurNote
        fields = ['name', 'description', 'me',]


class EntrepreneurNoteViewSet(viewsets.ModelViewSet):
    queryset = EntrepreneurNote.objects.all()
    serializer_class = EntrepreneurNoteSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, EmployeePermission, )
    filter_class = EntrepreneurNoteFilter
