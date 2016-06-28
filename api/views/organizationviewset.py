from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import generics, permissions, status, response, views, filters, mixins
from rest_framework.permissions import AllowAny
from api.serializers import OrganizationSerializer
from foundation.models.organization import Organization
from smegurus.settings import env_var


class OrganizationViewSet(generics.ListCreateAPIView):
    serializer_class = OrganizationSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [AllowAny,]
    queryset = User.objects.none() # Restrict so no-one sees the users.

    def perform_create(self, serializer):
        """
        Override the "create" functionality to use the "django-tenants"
        functionality for creating a new tenant.
        """
        tenant = Organization(
            schema_name=serializer.data['schema_name'],
            name=serializer.data['name'],
            # paid_until=serializer.data['paid_until'],
            on_trial=serializer.data['on_trial']
        )
        try:
            tenant.save() # migrate_schemas automatically called, your tenant is ready to be used!
        except Exception as e:
            pass  #print(e)
