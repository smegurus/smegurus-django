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
