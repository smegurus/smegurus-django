import django_filters
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from api.permissions import IsOwnerOrReadOnly
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant import TenantImageUploadSerializer
from foundation_tenant.models.imageupload import TenantImageUpload


class TenantImageUploadFilter(django_filters.FilterSet):
    class Meta:
        model = TenantImageUpload
        fields = ['created','last_modified',]


class TenantImageUploadViewSet(viewsets.ModelViewSet):
    queryset = TenantImageUpload.objects.all()
    serializer_class = TenantImageUploadSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_class = TenantImageUploadFilter

    def perform_create(self, serializer):
        """Add owner to the TenantImageUpload when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(
            owner=self.request.user,
            imagefile=self.request.data.get('imagefile')
        )
