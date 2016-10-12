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
        Override the "create" functionality to include creating a new Domain
        object associated with the newely created Organization. This Domain
        object is needed for "django-tenants" library to have.
        """
        # Pre-save action: Include the owner attribute directly, rather
        # than from request data.
        org = serializer.save(owner=self.request.user)

        # Perform a custom post-save action.
        if org:
            # Override custom default values.
            org.has_mentors = True
            org.has_perks = True
            org.is_setup = False

            # Attach our current logged in User for our Organization.
            org.users.add(self.request.user)
            org.save()
