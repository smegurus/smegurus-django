from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve, reverse
from tenant_reception.decorators import tenant_reception_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.decorators import tenant_required


@login_required(login_url='/en/login')
@tenant_required
@tenant_profile_required
@tenant_reception_required
def is_required_page(request):
    """Function will return either True or False depending if it meets decorator criteria."""
    from django.http import JsonResponse
    return JsonResponse({
        'access-granted':True
    })
