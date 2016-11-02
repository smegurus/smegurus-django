import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import ManagementOrAuthenticatedReadOnlyPermission
from api.serializers.foundation_tenant_base  import TagSerializer
from foundation_tenant.models.base.tag import Tag


class TagFilter(django_filters.FilterSet):
    class Meta:
        model = Tag
        fields = ['name', 'is_program',]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, ManagementOrAuthenticatedReadOnlyPermission, )
    filter_class = TagFilter
