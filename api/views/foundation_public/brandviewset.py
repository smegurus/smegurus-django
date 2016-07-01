import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers.foundation_public import PublicBrandSerializer
from foundation_public.models.brand import PublicBrand


class PublicBrandFilter(django_filters.FilterSet):
    class Meta:
        model = PublicBrand
        fields = ['created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url']


class PublicBrandViewSet(viewsets.ModelViewSet):
    queryset = PublicBrand.objects.all()
    serializer_class = PublicBrandSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    filter_class = PublicBrandFilter
