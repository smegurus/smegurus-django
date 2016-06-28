import django_filters
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from api.permissions import IsOwnerOrReadOnly
from api.pagination import LargeResultsSetPagination
from foundation.serializers import PublicImageUploadSerializer
from foundation.models.publicimageupload import PublicImageUpload


class PublicImageUploadFilter(django_filters.FilterSet):
    class Meta:
        model = PublicImageUpload
        fields = ['created','last_modified',]


class PublicImageUploadViewSet(viewsets.ModelViewSet):
    queryset = PublicImageUpload.objects.all()
    serializer_class = PublicImageUploadSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_class = PublicImageUploadFilter

    def perform_create(self, serializer):
        """Add owner to the PublicImageUpload when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(
            owner=self.request.user,
            imagefile=self.request.data.get('imagefile')
        )
