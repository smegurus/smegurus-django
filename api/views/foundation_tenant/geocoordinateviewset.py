import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers.foundation_tenant import GeoCoordinateSerializer
from foundation_tenant.models.geocoordinate import GeoCoordinate


class GeoCoordinateFilter(django_filters.FilterSet):
    class Meta:
        model = GeoCoordinate
        fields = ['created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'address', 'address_country', 'elevation', 'latitude', 'longitude', 'postal_code',]


class GeoCoordinateViewSet(viewsets.ModelViewSet):
    queryset = GeoCoordinate.objects.all()
    serializer_class = GeoCoordinateSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    filter_class = GeoCoordinateFilter
