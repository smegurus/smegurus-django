import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import EmployeePermission
from api.serializers.foundation_tenant_base  import InfoResourceSerializer
from foundation_tenant.models.base.inforesource import InfoResource


class InfoResourceFilter(django_filters.FilterSet):
    class Meta:
        model = InfoResource
        fields = ['created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'uploads', 'is_for_staff', 'is_for_entrepreneur', 'stage_num', 'tags',]


class InfoResourceViewSet(viewsets.ModelViewSet):
    queryset = InfoResource.objects.all()
    serializer_class = InfoResourceSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, EmployeePermission,)
    filter_class = InfoResourceFilter

    def perform_create(self, serializer):
        """Override the create command to add additional computations."""
        # Include the owner attribute directly, rather than from request data.
        info_resource = serializer.save(
            owner=self.request.user,
        )

    def perform_destroy(self, instance):
        """Override the deletion function to include deletion of associated models."""
        if instance.upload:
            instance.upload.delete()
        instance.delete()  # Delete our model.
