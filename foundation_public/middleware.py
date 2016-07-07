from django.http import HttpResponseForbidden
from foundation_public.models.banned import BannedIP
from foundation_public.models.me import PublicMe


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


class PublicMeMiddleware(object):
    def process_request(self, request):
        """
            The purpose of this middleware is to lookup the 'Me' object for
            the authenticated user and attach it to the request. If the user
            is authenticated and does not have a 'Me' object then it will be
            created in this middleware.
        """
        if request.user.is_authenticated():
            me, created = PublicMe.objects.get_or_create(owner=request.user)
            request.me = me

        return None  # Finish our middleware handler.
