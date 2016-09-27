import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers.foundation_public import PublicPostalAddressSerializer
from foundation_public.models.postaladdress import PublicPostalAddress


class PublicPostalAddressFilter(django_filters.FilterSet):
    class Meta:
        model = PublicPostalAddress
        fields = ['id', 'name', 'alternate_name', 'description', 'owner', 'url',
                  'country', 'postal_code', 'locality', 'region',
                  'street_number', 'suffix',
                  'street_name', 'street_type', 'direction', 'suite_number',
                  'floor_number', 'buzz_number', 'address_line_2',
                  'address_line_3',]


class PublicPostalAddressViewSet(viewsets.ModelViewSet):
    queryset = PublicPostalAddress.objects.all()
    serializer_class = PublicPostalAddressSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    filter_class = PublicPostalAddressFilter
