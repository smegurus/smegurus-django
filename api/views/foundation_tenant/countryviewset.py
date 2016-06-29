import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers.foundation_tenant import CountrySerializer
from foundation_tenant.models.country import Country


class CountryFilter(django_filters.FilterSet):
    class Meta:
        model = Country
        fields = ['created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url']


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_class = CountryFilter
