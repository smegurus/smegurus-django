import django_filters
from django.core.management import call_command
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, mixins
from rest_framework import filters
from rest_framework import permissions
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import detail_route
from rest_framework.decorators import detail_route
from rest_framework.authentication import TokenAuthentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwner
from api.serializers.foundation_public import PublicMeSerializer
from foundation_public.models.me import PublicMe


class PublicMeFilter(django_filters.FilterSet):
    class Meta:
        model = PublicMe
        fields = ['created', 'last_modified', 'owner',]


class PublicMeViewSet(viewsets.ModelViewSet):
    queryset = PublicMe.objects.all()
    serializer_class = PublicMeSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwner, )
    filter_class = PublicMeFilter

    @detail_route(methods=['put'], permission_classes=[IsOwner,])
    def unlock_me(self, request, pk=None):
        # Get our data.
        me = self.get_object()
        try:
            password = request.data['password']
        except Exception as e:
            return response.Response(
                data={'message': 'Missing password.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Test to see if the password entered works.
        authenticated_user = authenticate(
            username=me.owner.username,
            password=password
        )
        if authenticated_user:
            me.is_locked=False
            me.save()
            return response.Response(
                data={'message': 'User has unlocked'},
                status=status.HTTP_200_OK
            )
        else:
            return response.Response(
                data={'message': 'Failed authenticating'},
                status=status.HTTP_400_BAD_REQUEST
            )
