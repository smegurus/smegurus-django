import django_filters
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from api.permissions import ManagementOrAuthenticatedReadOnlyPermission
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant_base import FAQGroupSerializer
from foundation_tenant.models.base.faqgroup import FAQGroup


class FAQGroupFilter(django_filters.FilterSet):
    class Meta:
        model = FAQGroup
        fields = ['created','last_modified',]


class FAQGroupViewSet(viewsets.ModelViewSet):
    queryset = FAQGroup.objects.all()
    serializer_class = FAQGroupSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, ManagementOrAuthenticatedReadOnlyPermission)
    filter_class = FAQGroupFilter
