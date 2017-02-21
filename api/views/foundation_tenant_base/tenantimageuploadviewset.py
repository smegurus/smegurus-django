import django_filters
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from api.permissions import IsOwnerOrReadOnly
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant_base import ImageUploadSerializer
from foundation_tenant.models.base.imageupload import ImageUpload


class ImageUploadFilter(django_filters.FilterSet):
    class Meta:
        model = ImageUpload
        fields = ['created','last_modified',]


class ImageUploadViewSet(viewsets.ModelViewSet):
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_class = ImageUploadFilter

    def perform_create(self, serializer):
        """Add owner to the ImageUpload when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(
            owner=self.request.user,
            imagefile=self.request.data.get('imagefile')
        )
