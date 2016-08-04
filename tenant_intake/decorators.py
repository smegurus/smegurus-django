from functools import wraps
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from foundation_public import constants
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.me import TenantMe


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


def tenant_intake_has_completed_redirection_required(view_func):
    """
    Decorator will check to see if the User's Intake has been completed or not
    and if Intake has been completed then redirect to the final page, else
    allow the current page to load up.
    """
    def wrapper(request, *args, **kwargs):
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)

        # Check to see if the Me object is setup.
        if entrepreneur_group in request.user.groups.all():
            intake, created = Intake.objects.get_or_create(me=request.tenant_me)
            if intake.is_completed:
                return HttpResponseRedirect(reverse('tenant_intake_finished'))

        # Check to see if the current entrepreneur is setup.
        return view_func(request, *args, **kwargs)
    return wrapper
