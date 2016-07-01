import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers.foundation_public import PublicPlaceSerializer
from foundation_public.models.place import PublicPlace


class PublicPlaceFilter(django_filters.FilterSet):
    class Meta:
        model = PublicPlace
        fields = ['created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'address', 'fax_number', 'geo', 'global_location_number', 'has_map', 'isic_v4', 'logo', 'opening_hours_specification', 'photo', 'telephone',]


class PublicPlaceViewSet(viewsets.ModelViewSet):
    queryset = PublicPlace.objects.all()
    serializer_class = PublicPlaceSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    filter_class = PublicPlaceFilter
