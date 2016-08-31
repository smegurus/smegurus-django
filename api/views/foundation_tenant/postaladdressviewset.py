import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrIsAnEmployee
from api.serializers.foundation_tenant import PostalAddressSerializer
from foundation_tenant.models.postaladdress import PostalAddress


class PostalAddressFilter(django_filters.FilterSet):
    class Meta:
        model = PostalAddress
        fields = ['name', 'alternate_name', 'description', 'owner', 'url',
                 'address_country', 'is_address_country_other',
                 'address_locality', 'is_address_locality_other',
                 'address_region', 'is_address_region_other',
                 'post_office_box_number', 'postal_code', 'street_address',]


class PostalAddressViewSet(viewsets.ModelViewSet):
    queryset = PostalAddress.objects.all()
    serializer_class = PostalAddressSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrIsAnEmployee, )
    filter_class = PostalAddressFilter
