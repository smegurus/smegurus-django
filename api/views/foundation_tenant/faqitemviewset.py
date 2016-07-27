import django_filters
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from api.permissions import ManagementOrAuthenticatedReadOnlyPermission
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant import FAQItemSerializer
from foundation_tenant.models.faqitem import FAQItem


class FAQItemFilter(django_filters.FilterSet):
    class Meta:
        model = FAQItem
        fields = ['created','last_modified',]


class FAQItemViewSet(viewsets.ModelViewSet):
    queryset = FAQItem.objects.all()
    serializer_class = FAQItemSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, ManagementOrAuthenticatedReadOnlyPermission)
    filter_class = FAQItemFilter
