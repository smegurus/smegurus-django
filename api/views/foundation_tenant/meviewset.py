import django_filters
from django.core.management import call_command
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rest_framework import filters
from rest_framework import permissions
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers.foundation_tenant  import MeSerializer
from foundation_tenant.models.me import Me


class MeFilter(django_filters.FilterSet):
    class Meta:
        model = Me
        fields = ['created', 'last_modified', 'owner',]


class MeViewSet(viewsets.ModelViewSet):
    queryset = Me.objects.all()
    serializer_class = MeSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    filter_class = MeFilter


    @detail_route(methods=['get'], permission_classes=[IsOwnerOrReadOnly])
    def evaluate_me(self, request, pk=None):
        # call_command('evaluate_me',str(pk))
        return Response({'status': 'success', 'message': 'successfully ran game loop for user.'})