from functools import wraps
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect


def tenant_profile_required(view_func):
    """
    Decorator ensures any application logic associated with having the profile
    app setup to take precedence over the current view loaded up.
    """
    def wrapper(request, *args, **kwargs):
        if request.public_me.is_locked:
            return HttpResponseRedirect(reverse('tenant_profile_lock'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper
