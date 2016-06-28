import django_filters
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from api.permissions import IsOwnerOrReadOnly
from api.pagination import LargeResultsSetPagination
from api.serializers import PrivateFileUploadSerializer
from api.models.privatefileupload import PrivateFileUpload


class PrivateFileUploadFilter(django_filters.FilterSet):
    class Meta:
        model = PrivateFileUpload
        fields = ['created','last_modified','owner',]


class PrivateFileUploadViewSet(viewsets.ModelViewSet):
    queryset = PrivateFileUpload.objects.all()
    serializer_class = PrivateFileUploadSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_class = PrivateFileUploadFilter

    def perform_create(self, serializer):
        """Add owner to the PrivateFileUpload when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(
            owner=self.request.user,
            datafile=self.request.data.get('datafile')
        )
