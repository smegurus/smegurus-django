import django_filters
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import generics, permissions, status, response, views, filters, mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from api.serializers.foundation_public import PublicOrganizationSerializer
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly, IsOwnerOrIsAnEmployee, EmployeePermission, IsOwner, ManagerPermission
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

    @detail_route(methods=['post'], permission_classes=[IsOwner,])
    def enable_set_has_staff_checkin_required(self, request, pk=None):
        # Get our data.
        organization = self.get_object()
        try:
            organization.has_staff_checkin_required = True
            organization.save()
            return response.Response(
                data={'message': 'Enabled - set_has_staff_checkin_required'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return response.Response(
                data={'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['post'], permission_classes=[IsOwner,])
    def disable_set_has_staff_checkin_required(self, request, pk=None):
        # Get our data.
        organization = self.get_object()
        try:
            organization.has_staff_checkin_required = False
            organization.save()
            return response.Response(
                data={'message': 'Disabled - set_has_staff_checkin_required'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return response.Response(
                data={'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
