import django_filters
from django.contrib.auth.models import User
from django.core.management import call_command
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrIsAnEmployee, EmployeePermission
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

    @detail_route(methods=['post'], permission_classes=[EmployeePermission])
    def admit_me(self, request, pk=None):
        call_command('admit_me',str(pk))
        return Response({'status': status.HTTP_200_OK, 'message': 'User has been admitted.'})

    @detail_route(methods=['post'], permission_classes=[EmployeePermission])
    def expel_me(self, request, pk=None):
        call_command('expel_me',str(pk))
        return Response({'status': status.HTTP_200_OK, 'message': 'User has been expelled.'})
