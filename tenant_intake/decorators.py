from functools import wraps
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from smegurus import constants
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.me import TenantMe


def tenant_intake_required(view_func):
    """
    Decorater checks to see if the Entrepreneur has finished the Intake or not.
    If the Intake was done then do nothing, else redirect to Intake submission
    form.
    """
    def wrapper(request, *args, **kwargs):
        if request.tenant_me.is_entrepreneur():
            if request.tenant_me.is_in_intake:
                return HttpResponseRedirect(reverse('tenant_intake_entr_round_one_step_one'))

        return view_func(request, *args, **kwargs)
    return wrapper
