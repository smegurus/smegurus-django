import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers.foundation_tenant import PostalAddressSerializer
from foundation_tenant.models.postaladdress import PostalAddress


class PostalAddressFilter(django_filters.FilterSet):
    class Meta:
        model = PostalAddress
        fields = ['name', 'alternate_name', 'description', 'address_country', 'address_locality', 'address_region', 'post_office_box_number', 'postal_code', 'street_address', 'created', 'last_modified', 'owner',]


class PostalAddressViewSet(viewsets.ModelViewSet):
    queryset = PostalAddress.objects.all()
    serializer_class = PostalAddressSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    filter_class = PostalAddressFilter
