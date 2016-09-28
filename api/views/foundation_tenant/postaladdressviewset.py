import django_filters
from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import response
from rest_framework import status
from rest_framework.decorators import detail_route
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrIsAnEmployee
from api.serializers.foundation_tenant import PostalAddressSerializer
from foundation_tenant.models.postaladdress import PostalAddress


class PostalAddressFilter(django_filters.FilterSet):
    class Meta:
        model = PostalAddress
        fields = ['id', 'name', 'alternate_name', 'description', 'owner', 'url',
                  'country', 'postal_code', 'locality', 'region',
                  'street_number', 'suffix',
                  'street_name', 'street_type', 'direction', 'suite_number',
                  'floor_number', 'buzz_number', 'address_line_2',
                  'address_line_3',]


class PostalAddressViewSet(viewsets.ModelViewSet):
    queryset = PostalAddress.objects.all()
    serializer_class = PostalAddressSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrIsAnEmployee, )
    filter_class = PostalAddressFilter

    def perform_create(self, serializer):
        """Add owner to the object when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(
            owner=self.request.user,
        )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated,])
    def rebuild_geo_data(self, request, pk=None):
        postal_address = self.get_object()
        call_command('rebuild_tenant_postaladdress',str(postal_address.id))
        return response.Response(status=status.HTTP_200_OK)
