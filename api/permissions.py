from django.contrib.auth.models import User, AnonymousUser
from rest_framework import permissions
from foundation_public.models.banned import BannedIP
from api.constants import *


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


# class EmployeePermission(permissions.BasePermission):
#     """
#     Global permission check for authenticated User to see if they are an
#     Employee of this organization.
#     """
#     message = 'You are not an Employee!'
#     def has_permission(self, request, view):
#         if request.user.is_anonymous():
#             return False
#         else:
#             for group in request.user.groups.all():
#                 if group.name in EMPLOYEE_GROUPS:
#                     return True
#             return False
#
#
# class IsOwnerOrIsAnEmployee(permissions.BasePermission):
#     """
#     Object-level permission to only allow owners of an object to view/edit it.
#     However, if the authenticated User is an Employee then they also get
#     automatic read/write privilledges.
#     Assumes the model instance has an `owner` attribute.
#     """
#     message = 'Only owners are allowed to write data.'
#     def has_object_permission(self, request, view, obj):
#         # Step 1: Reject access to non-authenticated users.
#         if request.user.is_anonymous():
#             return False
#         else:
#             # Step 2: Allow access to Employees
#             for group in request.user.groups.all():
#                 if group.name in EMPLOYEE_GROUPS:
#                     return True
#
#             # Step 3: Allow accesss to the owners of the object.
#             # Instance must have an attribute named `owner`.
#             return obj.owner == request.user
