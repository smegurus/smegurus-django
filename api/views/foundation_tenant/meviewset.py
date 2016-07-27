import django_filters
from django.contrib.auth.models import User
from django.core.management import call_command
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import detail_route
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrIsAnEmployee, EmployeePermission, IsOwner
from api.serializers.foundation_tenant import TenantMeSerializer
from foundation_tenant.models.me import TenantMe


class TenantMeFilter(django_filters.FilterSet):
    class Meta:
        model = TenantMe
        fields = ['owner', 'tags',]


class TenantMeViewSet(viewsets.ModelViewSet):
    queryset = TenantMe.objects.all()
    serializer_class = TenantMeSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrIsAnEmployee, )
    filter_class = TenantMeFilter

    @detail_route(methods=['put'], permission_classes=[EmployeePermission])
    def admit_tenant_me(self, request, pk=None):
        call_command('admit_me',str(pk))
        return response.Response(
            data={'message': 'User has been admitted.'},
            status=status.HTTP_200_OK
        )

    @detail_route(methods=['put'], permission_classes=[EmployeePermission])
    def expel_tenant_me(self, request, pk=None):
        call_command('expel_me',str(pk))
        return response.Response(
            data={'message': 'User has been expelled.'},
            status=status.HTTP_200_OK
        )

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
