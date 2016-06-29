from functools import wraps
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden


def tenant_required(view_func):
    """Decorator ensures an subdomain is associated with the view request."""
    def wrapper(request, *args, **kwargs):
        if request.tenant.schema_name != "public":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Missing tenant.")
    return wrapper
