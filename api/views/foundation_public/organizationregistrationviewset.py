import django_filters
from django.contrib.auth.models import User
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
        # Pre-save action: Include the owner attribute directly, rather
        # than from request data.
        org = serializer.save()

    
        from api.tasks import begin_organization_creation_task
        begin_organization_creation_task.delay(org.id)
