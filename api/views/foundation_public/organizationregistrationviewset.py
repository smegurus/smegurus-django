import django_filters
from django.contrib.auth.models import User
from django.db import connection # Used for django tenants.
from rest_framework import authentication
from rest_framework import generics, permissions, status, response, views, filters, mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.serializers.foundation_public import PublicOrganizationRegistrationSerializer
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from foundation_public.models.organizationregistration import PublicOrganizationRegistration
from foundation_public.models.contactpoint import PublicContactPoint
from foundation_public.models.postaladdress import PublicPostalAddress
from smegurus.settings import env_var


class PublicOrganizationRegistrationFilter(django_filters.FilterSet):
    class Meta:
        model = PublicOrganizationRegistration
        fields = ['owner', 'name',]


class PublicOrganizationRegistrationViewSet(viewsets.ModelViewSet):
    queryset = PublicOrganizationRegistration.objects.all()
    serializer_class = PublicOrganizationRegistrationSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = PublicOrganizationRegistrationFilter

    def perform_create(self, serializer):
        """
        Override the "create" functionality to include ...
        """
        # Connection needs first to be at the public schema, as this is where
        # the database needs to be set before creating a new tenant. If this is
        # not done then django-tenants will raise a "Can't create tenant outside
        # the public schema." error.
        connection.set_schema_to_public() # Switch to Public.

        # Pre-save action: Include the owner attribute directly, rather
        # than from request data.
        org = serializer.save()

        # Populate the organization in an asynch process.
        import django_rq
        from api.tasks import begin_organization_creation_task
        django_rq.enqueue(update_balance_owing_amount_for_associate_func,
            org.id
        )
