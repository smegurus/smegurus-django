from django.http import HttpResponseForbidden
from foundation_public.models.banned import BannedIP


class BanEnforcingMiddleware(object):
    def process_request(self, request):
        """
        Check the current IP of the connected User and if the IP matches a
        banned IP then deny access to the site.
        """
        ip_addr = request.META['REMOTE_ADDR']
        banned = BannedIP.objects.filter(address=ip_addr).exists()

        if banned:
            return HttpResponseForbidden('You are banned.')
        else:
            return None