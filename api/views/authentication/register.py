from django.contrib.auth.models import User, Group
from django.core.management import call_command
from rest_framework import generics, permissions, status, response, views, filters, mixins
from rest_framework.permissions import AllowAny
from api.serializers.authentication import RegisterSerializer
from foundation_public.models.organization import PublicOrganization
from foundation_public.constants import *


class RegisterViewSet(generics.ListCreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny,]
    queryset = User.objects.none() # Restrict so no-one sees the users.

    def perform_create(self, serializer):
        """
        1. Save User.
        2. Assign User to specific Group based on Tenant.
        3. Assign User to specific PublicOrganization.
        """
        user = serializer.save()  # Save the User model from the serializer.

        # Assign the User to the specific Group depending on whether the
        # User was regisered from the Tenant or on the Public schema.
        group = None
        if self.request.tenant.schema_name == 'public' or self.request.tenant.schema_name == 'test':
            group = Group.objects.get(id=ORGANIZATION_ADMIN_GROUP_ID)
        else:
            group = Group.objects.get(id=ENTREPRENEUR_GROUP_ID)
        # print("Attaching to Group:", group)
        user.groups.add(group)
        user.save()

        # Assign the User membership into the specific Organization.
        if self.request.tenant.schema_name != 'public' and self.request.tenant.schema_name != 'test':
            # print("Attaching to Organization:", self.request.tenant.schema_name)
            self.request.tenant.users.add(user)
            self.request.tenant.save()

        # Send activation emails.
        call_command('send_public_activation_email',str(user.email))
