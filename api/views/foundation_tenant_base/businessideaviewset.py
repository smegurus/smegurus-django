import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers.foundation_tenant_base  import BusinessIdeaSerializer
from foundation_tenant.models.base.businessidea import BusinessIdea


class BusinessIdeaFilter(django_filters.FilterSet):
    class Meta:
        model = BusinessIdea
        fields = ['owner', 'name', 'industry',]


class BusinessIdeaViewSet(viewsets.ModelViewSet):
    queryset = BusinessIdea.objects.all()
    serializer_class = BusinessIdeaSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
    filter_class = BusinessIdeaFilter

    def perform_create(self, serializer):
        """Add owner to the BusinessIdea when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(
            owner=self.request.user,
        )
