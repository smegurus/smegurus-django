import django_filters
from django.contrib.auth.models import User
from django.core.management import call_command
from django.contrib.auth import authenticate, login, logout
from rest_framework import exceptions
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import detail_route
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrIsAnEmployee, EmployeePermission, IsOwner, ManagerPermission
from api.serializers.foundation_tenant import TenantMeSerializer
from api.serializers.misc import JSONDictionarySerializer
from foundation_tenant.models.base.me import TenantMe
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.contactpoint import ContactPoint
from smegurus import constants


class TenantMeFilter(django_filters.FilterSet):
    class Meta:
        model = TenantMe
        fields = ['owner', 'tags', 'stage_num',]


class TenantMeViewSet(viewsets.ModelViewSet):
    queryset = TenantMe.objects.all()
    serializer_class = TenantMeSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrIsAnEmployee, )
    filter_class = TenantMeFilter

    def perform_update(self, serializer):
        """Update "TenantMe" model and its associated models."""
        # Update the 'TenantMe' model.
        me = serializer.save()
        me.name = me.given_name + " " + me.family_name
        me.save()

        # Update the "User" model.
        me.owner.first_name = me.given_name
        me.owner.last_name = me.family_name
        me.owner.email = me.email
        me.owner.save()

        # Update the "ContactPoint" model.
        me.contact_point.telephone = me.telephone
        me.contact_point.email = me.email
        me.contact_point.save()

    def perform_destroy(self, instance):
        """Override the deletion function to include deletion of associated models."""
        # Defensive Code: Prevent deletion of upper-tier management members.
        for target_group_id in [constants.ORGANIZATION_ADMIN_GROUP_ID, constants.CLIENT_MANAGER_GROUP_ID, constants.SYSTEM_ADMIN_GROUP_ID]:
            for search_group in instance.owner.groups.all():
                if target_group_id == search_group.id:
                    raise exceptions.ParseError("Cannot delete upper-tier management user.")

        # Delete objects which are dependent on this model.
        try:
            intake = Intake.objects.get(me=instance)
            intake.delete()
        except Intake.DoesNotExist:
            pass

        try:
            postal_address = PostalAddress.objects.get(owner=instance.owner)
            postal_address.delete()
        except PostalAddress.DoesNotExist:
            pass

        try:
            contact_point = ContactPoint.objects.get(owner=instance.owner)
            contact_point.delete()
        except ContactPoint.DoesNotExist:
            pass

        # Delete the User object which will cascade the deletions to other objects.
        instance.owner.delete()

    @detail_route(methods=['put'], permission_classes=[EmployeePermission])
    def admit_me(self, request, pk=None):
        call_command('admit_me',str(pk))
        return response.Response(
            data={'message': 'User has been admitted.'},
            status=status.HTTP_200_OK
        )

    @detail_route(methods=['put'], permission_classes=[EmployeePermission])
    def expel_me(self, request, pk=None):
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


    @detail_route(methods=['put'], permission_classes=[ManagerPermission,])
    def set_roles(self, request, pk=None):
        """Function allows setting the roles an employee belongs to by the manager."""
        try:
            serializer = JSONDictionarySerializer(data=request.data)
            if serializer.is_valid():
                me = self.get_object()
                roles = serializer.data['array']
                for group_id in roles:
                    me.owner.groups.add(int(group_id))
                me.save()
            return response.Response(
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
