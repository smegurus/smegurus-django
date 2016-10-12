from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.utils.translation import get_language
from foundation_public.models.banned import BannedIP
from foundation_public.models.visitor import PublicVisitor
from foundation_public import constants


class TrapURLBanningMiddleware(object):
    """Automatically ban IP's attempting to access suspicious URLs."""
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.path in constants.SUSPICIOUS_PATHS:
            ip_addr = self.get_client_ip(request)
            BannedIP.objects.create(
                address=ip_addr,
                reason=request.path
            )
            return HttpResponseForbidden('You are banned.')
        else:
            return self.get_response(request)


class BanEnforcingMiddleware(object):
    """
    Check the current IP of the connected User and if the IP matches a
    banned IP then deny access to the site.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        banned = BannedIP.objects.filter(address=request.ip_address).exists()
        if banned:
            return HttpResponseForbidden('You are banned.')
        else:
            return self.get_response(request)
