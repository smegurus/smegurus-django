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
from foundation_public.models.contactpoint import PublicContactPoint
from foundation_public.models.postaladdress import PublicPostalAddress
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
        contact_point = PublicContactPoint.objects.create(owner=self.request.user)
        address = PublicPostalAddress.objects.create(owner=self.request.user)

        # Pre-save action: Include the owner attribute directly, rather
        # than from request data.
        org = serializer.save(
            owner=self.request.user,
            contact_point=contact_point,
            address=address,
        )

        # Perform a custom post-save action.
        if org:
            # Our tenant requires a domain so create it here.
            from django.contrib.sites.models import Site
            from foundation_public.models.organization import PublicDomain
            domain = PublicDomain()
            domain.domain = org.schema_name + '.' + Site.objects.get_current().domain
            domain.tenant = org
            domain.is_primary = False
            domain.save()

            # Override custom default values.
            org.has_mentors = True
            org.has_perks = True
            org.is_setup = False

            # Attach our current logged in User for our Organization.
            org.users.add(self.request.user)
            org.save()

    # def perform_create(self, serializer):
    #     """
    #     Override the "create" functionality to include creating a new Domain
    #     object associated with the newely created Organization. This Domain
    #     object is needed for "django-tenants" library to have.
    #     """
    #     contact_point, created = PublicContactPoint.objects.get_or_create(owner=self.request.user)
    #     address, created = PublicPostalAddress.objects.get_or_create(owner=self.request.user)
    #
    #     dict = {
    #         'schema_name': 'test',
    #         'name': '',
    #         'alternate_name': '',
    #         'legal_name': '',
    #         'is_tos_signed': True
    #     }
    #
    #     print("----------------------------------------FINISHED----------------------------------------")
    #
    #     # Asynchronously create our tenant in the background.
    #     # from api.tasks import begin_organization_creation_task
    #     # begin_organization_creation_task.delay(dict)
