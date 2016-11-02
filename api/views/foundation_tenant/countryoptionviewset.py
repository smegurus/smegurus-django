import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers.foundation_tenant import CountryOptionSerializer
from foundation_tenant.models.base.countryoption import CountryOption


class TenantCountryOptionFilter(django_filters.FilterSet):
    class Meta:
        model = CountryOption
        fields = ['name',]


class TenantCountryOptionViewSet(viewsets.ModelViewSet):
    queryset = CountryOption.objects.all()
    serializer_class = CountryOptionSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_class = TenantCountryOptionFilter
