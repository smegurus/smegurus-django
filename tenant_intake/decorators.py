from functools import wraps
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from foundation_public import constants


def tenant_intake_required(view_func):
    def wrapper(request, *args, **kwargs):
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        # org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)

        # Check to see if the Me object is setup.
        if entrepreneur_group in request.user.groups.all():
            if not request.tenant_me.is_admitted:
                return HttpResponseRedirect(reverse('tenant_intake_entr_step_one'))

        # Check to see if the current entrepreneur is setup.
        return view_func(request, *args, **kwargs)
    return wrapper
