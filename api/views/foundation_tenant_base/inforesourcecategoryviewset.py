import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import EmployeePermission
from api.serializers.foundation_tenant_base  import InfoResourceCategorySerializer
from foundation_tenant.models.base.inforesourcecategory import InfoResourceCategory


class InfoResourceCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = InfoResourceCategory
        fields = ['created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url',]


class InfoResourceCategoryViewSet(viewsets.ModelViewSet):
    queryset = InfoResourceCategory.objects.all()
    serializer_class = InfoResourceCategorySerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, EmployeePermission,)
    filter_class = InfoResourceCategoryFilter

    def perform_create(self, serializer):
        """Override the create command to add additional computations."""
        # Include the owner attribute directly, rather than from request data.
        info_resource = serializer.save(
            owner=self.request.user,
        )
