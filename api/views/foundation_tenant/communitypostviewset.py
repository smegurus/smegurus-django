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
from api.serializers.foundation_tenant import CommunityPostSerializer
from foundation_tenant.models.communitypost import CommunityPost


class CommunityPostFilter(django_filters.FilterSet):
    class Meta:
        model = CommunityPost
        fields = ['created','last_modified',]


class CommunityPostViewSet(viewsets.ModelViewSet):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    filter_class = CommunityPostFilter

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
