import django_filters
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import generics, permissions, status, response, views, filters, mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.serializers.foundation_public import PublicOrganizationSerializer
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from foundation_public.models.organization import PublicOrganization
from smegurus.settings import env_var


class PublicOrganizationFilter(django_filters.FilterSet):
    class Meta:
        model = PublicOrganization
        fields = ['owner', 'name',]


class PublicOrganizationViewSet(viewsets.ModelViewSet):
    queryset = PublicOrganization.objects.all()
    serializer_class = PublicOrganizationSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = PublicOrganizationFilter


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
