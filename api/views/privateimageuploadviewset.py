import django_filters
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from api.permissions import IsOwnerOrReadOnly
from api.pagination import LargeResultsSetPagination
from api.serializers import PrivateImageUploadSerializer
from api.models.privateimageupload import PrivateImageUpload


class PrivateImageUploadFilter(django_filters.FilterSet):
    class Meta:
        model = PrivateImageUpload
        fields = ['created','last_modified',]


class PrivateImageUploadViewSet(viewsets.ModelViewSet):
    queryset = PrivateImageUpload.objects.all()
    serializer_class = PrivateImageUploadSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_class = PrivateImageUploadFilter

    def perform_create(self, serializer):
        """Add owner to the PrivateImageUpload when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(
            owner=self.request.user,
            imagefile=self.request.data.get('imagefile')
        )
