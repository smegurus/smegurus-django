import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers.foundation_tenant_bizmula import WorkspaceSerializer
from foundation_tenant.models.bizmula.workspace import Workspace


class WorkspaceFilter(django_filters.FilterSet):
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'owners',]


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_class = WorkspaceFilter
