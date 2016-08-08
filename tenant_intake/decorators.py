from functools import wraps
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from smegurus import constants
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.me import TenantMe


def tenant_intake_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.tenant_me.is_entrepreneur():
            if not request.tenant_me.is_admitted:
                return HttpResponseRedirect(reverse('tenant_intake_entr_step_one'))

        return view_func(request, *args, **kwargs)
    return wrapper


def tenant_intake_has_completed_redirection_required(view_func):
    """
    Decorator will check to see if the User's Intake has been completed or not
    and if Intake has been completed then redirect to the final page, else
    allow the current page to load up.
    """
    def wrapper(request, *args, **kwargs):
        if request.tenant_me.is_entrepreneur():
            intake, created = Intake.objects.get_or_create(me=request.tenant_me)
            if intake.status == constants.PENDING_REVIEW_STATUS:
                return HttpResponseRedirect(reverse('tenant_intake_finished'))

        return view_func(request, *args, **kwargs)
    return wrapper
