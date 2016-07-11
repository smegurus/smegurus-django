from functools import wraps
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from foundation_public import constants


def foundation_config_required(view_func):
    """
    Decorator ensures Organization associated with the view request has been
    setup else redirect it to this application.
    """
    def wrapper(request, *args, **kwargs):
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)

        # Check to see if the current Organization is setup and if it is not
        # then load up the Organization setup page for the Organization Admin
        # user.
        if org_admin_group in request.user.groups.all():
            if request.tenant.schema_name != "public" and request.tenant.schema_name != "test":
                if not request.tenant.is_setup:
                    return HttpResponseRedirect(reverse('foundation_auth_config_org_step_one'))

        # Check to see if the Me object is setup.
        elif org_admin_group in request.user.groups.all():
            pass #TODO: Implement.

        # Check to see if the current entrepreneur is setup.
        return view_func(request, *args, **kwargs)
    return wrapper
