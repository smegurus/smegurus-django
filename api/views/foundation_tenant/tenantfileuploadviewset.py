import django_filters
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from api.permissions import IsOwnerOrReadOnly
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant import TenantFileUploadSerializer
from foundation_tenant.models.fileupload import TenantFileUpload


class TenantFileUploadFilter(django_filters.FilterSet):
    class Meta:
        model = TenantFileUpload
        fields = ['created','last_modified','owner',]


class TenantFileUploadViewSet(viewsets.ModelViewSet):
    queryset = TenantFileUpload.objects.all()
    serializer_class = TenantFileUploadSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_class = TenantFileUploadFilter

    def perform_create(self, serializer):
        """Add owner to the TenantFileUpload when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(
            owner=self.request.user,
            datafile=self.request.data.get('datafile')
        )
