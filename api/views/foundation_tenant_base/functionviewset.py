from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.management import call_command
from rest_framework import permissions, status, response, views
from api.permissions import EmployeePermission


class FinalizeTenantSetupFunctionViewSet(views.APIView):
    """Populatest the associated data required for the Tenant."""
    permission_classes = [permissions.IsAuthenticated, EmployeePermission]

    def post(self, request):
        call_command('populate_tenant')
        call_command('populate_bizmula')
        call_command('naics_import')

        return response.Response(
            status=status.HTTP_200_OK
        )
