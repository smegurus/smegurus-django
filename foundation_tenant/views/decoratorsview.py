from django.http import JsonResponse
from foundation.decorators import tenant_required


@tenant_required
def tenant_is_valid(request):
    """Function will return either True or False depending if a subdomain exists or not."""
    return JsonResponse({
        'access-granted':True
    })
