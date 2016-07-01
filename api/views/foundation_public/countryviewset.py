import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers.foundation_public import PublicCountrySerializer
from foundation_public.models.country import PublicCountry


class PublicCountryFilter(django_filters.FilterSet):
    class Meta:
        model = PublicCountry
        fields = ['created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url']


class PublicCountryViewSet(viewsets.ModelViewSet):
    queryset = PublicCountry.objects.all()
    serializer_class = PublicCountrySerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_class = PublicCountryFilter
