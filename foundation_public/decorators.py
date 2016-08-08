from functools import wraps
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from smegurus import constants


def tenant_required(view_func):
    """Decorator ensures an subdomain is associated with the view request."""
    def wrapper(request, *args, **kwargs):
        if request.tenant.schema_name != "public" and request.tenant.schema_name != "test":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(
                _("Missing tenant.")
            )
    return wrapper


def group_required(group_id_list):
    def decorator(func):
        def inner(request, *args, **kwargs):
            if request.user.is_authenticated():  # Only run if logged in.
                for target_group_id in group_id_list:
                    for search_group in request.user.groups.all():
                        if search_group.id == target_group_id:
                            return func(request, *args, **kwargs)  # Return with success.
            # Return error.
            return HttpResponseForbidden(
                _("You do not belong to a particular group.")
            )
        return inner
    return decorator
