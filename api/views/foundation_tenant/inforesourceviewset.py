import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers.foundation_tenant  import InfoResourceSerializer
from foundation_tenant.models.inforesource import InfoResource


class InfoResourceFilter(django_filters.FilterSet):
    class Meta:
        model = InfoResource
        fields = ['created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'type_of', 'upload',]


class InfoResourceViewSet(viewsets.ModelViewSet):
    queryset = InfoResource.objects.all()
    serializer_class = InfoResourceSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    filter_class = InfoResourceFilter

    def perform_create(self, serializer):
        """Override the create command to add additional computations."""
        # Include the owner attribute directly, rather than from request data.
        info_resource = serializer.save(
            owner=self.request.user,
        )
