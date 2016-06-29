import django_filters
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from api.permissions import IsOwnerOrReadOnly
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_public import PublicFileUploadSerializer
from foundation_public.models.fileupload import PublicFileUpload


class PublicFileUploadFilter(django_filters.FilterSet):
    class Meta:
        model = PublicFileUpload
        fields = ['created','last_modified','owner',]


class PublicFileUploadViewSet(viewsets.ModelViewSet):
    queryset = PublicFileUpload.objects.all()
    serializer_class = PublicFileUploadSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_class = PublicFileUploadFilter

    def perform_create(self, serializer):
        """Add owner to the PublicFileUpload when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(
            owner=self.request.user,
            datafile=self.request.data.get('datafile')
        )
