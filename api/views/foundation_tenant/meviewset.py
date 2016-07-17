import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers.foundation_tenant import TenantMeSerializer
from foundation_tenant.models.me import TenantMe


class TenantMeFilter(django_filters.FilterSet):
    class Meta:
        model = TenantMe
        fields = ['owner', 'tags',]


class TenantMeViewSet(viewsets.ModelViewSet):
    queryset = TenantMe.objects.all()
    serializer_class = TenantMeSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    filter_class = TenantMeFilter
