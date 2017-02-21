import django_filters
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from api.permissions import IsOwnerOrReadOnly
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant_base import FileUploadSerializer
from foundation_tenant.models.base.fileupload import FileUpload


class FileUploadFilter(django_filters.FilterSet):
    class Meta:
        model = FileUpload
        fields = ['created','last_modified','owner',]


class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_class = FileUploadFilter

    def perform_create(self, serializer):
        """Add owner to the FileUpload when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(
            owner=self.request.user,
            datafile=self.request.data.get('datafile')
        )
