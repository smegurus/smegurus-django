import pytz
from django.utils import timezone
from django.http import HttpResponseForbidden
from foundation_public.models.banned import BannedIP
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.imageupload import TenantImageUpload
from foundation_tenant.models.visitor import TenantVisitor


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
