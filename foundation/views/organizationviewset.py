import django_filters
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import generics, permissions, status, response, views, filters, mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from foundation.serializers import OrganizationSerializer
from foundation.models.organization import Organization
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from smegurus.settings import env_var


class OrganizationFilter(django_filters.FilterSet):
    class Meta:
        model = Organization
        fields = ['owner', 'name',]


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = OrganizationFilter


    def perform_create(self, serializer):
        """
        Override the "create" functionality to use the "django-tenants"
        functionality for creating a new tenant.
        """
        tenant = Organization(
            schema_name=serializer.data['schema_name'],
            name=serializer.data['name'],
            # paid_until=serializer.data['paid_until'],
            on_trial=serializer.data['on_trial']
        )
        try:
            tenant.save() # migrate_schemas automatically called, your tenant is ready to be used!
        except Exception as e:
            pass  #print(e)
