from django.contrib.auth.models import User, AnonymousUser
from rest_framework import permissions
from smegurus import constants
from foundation_public.models.banned import BannedIP


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to read/edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'Only owners of the object are allowed to read/write.'
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous():
            return False
        else:
            return obj.owner == request.user  # Instance must have an attribute named `owner`.


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'Only owners are allowed to write data.'
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class IsAdminUserOrReadOnly(permissions.BasePermission):
    message = 'Only administrators are allowed to write data.'
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else: # Check permissions for write request
            if request.user.is_anonymous():
                return False
            else:
                return request.user.is_superuser


class ManagementOrAuthenticatedReadOnlyPermission(permissions.BasePermission):
    """
    Global permission check for authenticated User only:

    1. Users belonging to a Management Group will be granted WRITE functions.
    2. All other users will be granted READ functions.
    3. Non-authenticated Users will be denied all functionality.
    """
    message = 'You must be in a Management Group to write data, else you \
               must be authenticated in our system to read the data.'

    def has_permission(self, request, view):
        # CASE 1: Restrict non authenticated users.
        if request.user.is_anonymous():
            #print("ManagementOrAuthenticatedReadOnlyPermission: Is AnonymousUser")
            return False

        # CASE 2: Allow authenticated users.
        else:
            # CASE 2a: Allow "Read" functions.
            if request.method in permissions.SAFE_METHODS:
                #print("ManagementOrAuthenticatedReadOnlyPermission: Is Safe Function")
                return True

            # CASE 2b: Restrict "Write" functions.
            for group in request.user.groups.all():
                if group.id in constants.MANAGEMENT_EMPLOYEE_GROUP_IDS:
                    #print("ManagementOrAuthenticatedReadOnlyPermission: Is Management")
                    return True
            #print("ManagementOrAuthenticatedReadOnlyPermission: Is Not in Management:", request.user.groups.all())
            return False


class EmployeePermission(permissions.BasePermission):
    """
    Global permission check for authenticated User to see if they are an
    Employee of this organization.
    """
    message = 'You are not an Employee!'
    def has_permission(self, request, view):
        if request.user.is_anonymous():
            return False
        else:
            for group in request.user.groups.all():
                if group.id in constants.EMPLOYEE_GROUP_IDS:
                    return True
            return False


class IsOwnerOrIsAnEmployee(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to view/edit it.
    However, if the authenticated User is an Employee then they also get
    automatic read/write privilledges.

    Assumes the model instance has an `owner` attribute.
    """
    message = 'Only owners are allowed to write data.'
    def has_object_permission(self, request, view, obj):
        # Step 1: Reject access to non-authenticated users.
        if request.user.is_anonymous():
            return False
        else:
            # Step 2: Allow access to Employees
            for group in request.user.groups.all():
                if group.id in constants.EMPLOYEE_GROUP_IDS:
                    return True

            # Step 3: Allow accesss to the owners of the object.
            # Instance must have an attribute named `owner`.
            return obj.owner == request.user

class IsMessageObjectPermission(permissions.BasePermission):
    """
    Object-level permission to only allow Sender read/edit it while the
    Recipient can only read the message.

    (1) Assume User is authenticated.
    (2) Assume this model object has 'sender' and 'receipient'.
    (3) Assume request has a 'me' object which was authenticated.
    """
    message = 'Only owners of the object are allowed to read/write.'
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous():
            return False
        else:
            if "PUT" in request.method:
                return obj.sender == request.tenant_me

            return obj.sender == request.tenant_me or obj.recipient == request.tenant_me


class IsMe(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to read/edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'Only owners of the object are allowed to read/write.'
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous():
            return False
        else:
            return obj.me == request.tenant_me


class IsMeOrIsAnEmployee(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to view/edit it.
    However, if the authenticated User is an Employee then they also get
    automatic read/write privilledges.

    Assumes the model instance has an `me` attribute.
    """
    message = 'Only owners are allowed to write data.'
    def has_object_permission(self, request, view, obj):
        # Step 1: Reject access to non-authenticated users.
        if request.user.is_anonymous():
            return False
        else:
            # Step 2: Allow access to Employees
            for group in request.tenant_me.owner.groups.all():
                if group.id in constants.EMPLOYEE_GROUP_IDS:
                    return True

            # Step 3: Allow accesss to the owners of the object.
            # Instance must have an attribute named `owner`.
            return obj.me == request.tenant_me
