from django.http import JsonResponse
from foundation_public.decorators import tenant_required
from foundation_public.decorators import group_required
from foundation_public import constants


@tenant_required
def tenant_is_valid(request):
    """Function will return either True or False depending if a subdomain exists or not."""
    return JsonResponse({
        'access-granted':True
    })


@group_required([constants.ENTREPRENEUR_GROUP_ID, ])
def group_is_entrepreneur(request):
    """Function will return either True or False depending if the authenticated user is a Entreprenuer."""
    return JsonResponse({
        'is-entrepreneur':True
    })


@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID, ])
def group_is_org_admin(request):
    """Function will return either True or False depending if the authenticated user is a Org Admin."""
    return JsonResponse({
        'is-org-admin':True
    })
