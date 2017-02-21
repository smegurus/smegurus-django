from functools import wraps
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from smegurus import constants
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.me import Me


def tenant_reception_required(view_func):
    """
    Decorator will check to see if the User's Intake has been completed or not
    and if Intake has been completed then redirect to the reception page, else
    allow the current page to load up.
    """
    def wrapper(request, *args, **kwargs):
        if request.tenant_me.is_entrepreneur():
            if request.tenant_me.stage_num <= constants.ME_ONBOARDING_STAGE_NUM:
                return HttpResponseRedirect(reverse('tenant_reception'))
        return view_func(request, *args, **kwargs)
    return wrapper
