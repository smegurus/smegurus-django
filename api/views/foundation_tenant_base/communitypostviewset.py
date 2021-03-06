import django_filters
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import detail_route
from api.permissions import EmployeePermission, IsOwner, IsOwnerOrReadOnly
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant_base import CommunityPostSerializer
from foundation_tenant.models.base.communitypost import CommunityPost


class CommunityPostViewSet(viewsets.ModelViewSet):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'description',)

    def perform_create(self, serializer):
        """Add owner to this model when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(
            owner=self.request.user,
            me=self.request.tenant_me,
        )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated, IsOwner])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likers.add(request.user)
        post.save()
        return response.Response(
            data={'message': 'Item has been liked.'},
            status=status.HTTP_200_OK
        )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated, IsOwner])
    def unlike(self, request, pk=None):
        post = self.get_object()
        post.likers.remove(request.user)
        post.save()
        return response.Response(
            data={'message': 'Item has been unliked.'},
            status=status.HTTP_200_OK
        )
