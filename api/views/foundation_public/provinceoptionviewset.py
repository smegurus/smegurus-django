import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers.foundation_public import ProvinceOptionSerializer
from foundation_public.models.countryoption import CountryOption
from foundation_public.models.provinceoption import ProvinceOption


class PublicProvinceOptionFilter(django_filters.FilterSet):
    class Meta:
        model = ProvinceOption
        fields = ['name', 'country']


class PublicProvinceOptionViewSet(viewsets.ModelViewSet):
    queryset = ProvinceOption.objects.all()
    serializer_class = ProvinceOptionSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_class = PublicProvinceOptionFilter
