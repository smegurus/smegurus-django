import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers.foundation_public import PublicGeoCoordinateSerializer
from foundation_public.models.geocoordinate import PublicGeoCoordinate


class PublicGeoCoordinateFilter(django_filters.FilterSet):
    class Meta:
        model = PublicGeoCoordinate
        fields = ['created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'address', 'address_country', 'elevation', 'latitude', 'longitude', 'postal_code',]


class PublicGeoCoordinateViewSet(viewsets.ModelViewSet):
    queryset = PublicGeoCoordinate.objects.all()
    serializer_class = PublicGeoCoordinateSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    filter_class = PublicGeoCoordinateFilter
