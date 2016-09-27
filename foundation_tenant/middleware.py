import pytz
from django.utils import timezone
from django.http import HttpResponseForbidden
from foundation_public.models.banned import BannedIP
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.imageupload import TenantImageUpload
from foundation_tenant.models.visitor import TenantVisitor


class TenantTimezoneMiddleware(object):
    def process_request(self, request):
        """Sets the timezone per Organization."""
        if not request.tenant.schema_name in ['public', 'test']:
            # Source:
            # https://docs.djangoproject.com/en/dev/topics/i18n/timezones/#selecting-the-current-time-zone
            tzname = request.tenant.time_zone
            timezone.activate(pytz.timezone(tzname))
        return None  # Finish our middleware handler.


class TenantMeMiddleware(object):
    def process_request(self, request):
        """
            The purpose of this middleware is to lookup the 'Me' object for
            the authenticated user and attach it to the request. If the user
            is authenticated and does not have a 'Me' object then it will be
            created in this middleware.
        """
        if not request.tenant.schema_name in ['public', 'test']:
            if request.user.is_authenticated():
                # STEP 1: Get or create a TenantMe.
                tenant_me, created = TenantMe.objects.get_or_create(owner=request.user)
                request.tenant_me = tenant_me
        return None  # Finish our middleware handler.


class TenantVisitorMiddleware(object):
    def get_client_ip(self, request):
        """Utility function for getting the IP. Source: http://stackoverflow.com/a/4581997"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def process_request(self, request):
        """Function will save the visitor for the this tenant."""
        if not request.tenant.schema_name in ['public', 'test']:
            if request.user.is_authenticated():
                request.visitor = TenantVisitor.objects.create(
                    me=request.tenant_me,
                    path=request.path,
                    ip_address=self.get_client_ip(request)
                )
