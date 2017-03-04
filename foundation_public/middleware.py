# -*- coding: utf-8 -*-
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
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
            BannedIP.objects.create(
                address=request.ip_address,
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


class NoSniffMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        return response


class DefaultLanguageRedirectMiddleware(object):
    """
        BUGFIX Middleware:
        For some reason when the landpage is accessed with Django 1.10.x
        the framework does not redirect to the default 'English' landpage.
        As a result, this class must be used unil the bug is fixed.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_url = request.get_full_path()  # Get the current URL.

        # Detect the homepage has been landed on without default langauge.
        if len(user_url) and user_url == "/":
            return HttpResponseRedirect(reverse('public_home'))
        return self.get_response(request)
