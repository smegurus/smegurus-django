import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers.foundation_tenant_base import CityOptionSerializer
from foundation_tenant.models.base.countryoption import CountryOption
from foundation_tenant.models.base.provinceoption import ProvinceOption
from foundation_tenant.models.base.cityoption import CityOption


class TenantCityOptionFilter(django_filters.FilterSet):
    class Meta:
        model = CityOption
        fields = ['name', 'country', 'province',]


class TenantCityOptionViewSet(viewsets.ModelViewSet):
    queryset = CityOption.objects.all()
    serializer_class = CityOptionSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_class = TenantCityOptionFilter
