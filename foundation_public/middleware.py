from django.http import HttpResponseForbidden
from foundation_public.models.banned import BannedIP
from foundation_public.models.visitor import PublicVisitor
from foundation_public import constants


class PublicBanEnforcingMiddleware(object):
    def process_request(self, request):
        """
        Check the current IP of the connected User and if the IP matches a
        banned IP then deny access to the site.
        """
        banned = BannedIP.objects.filter(address=request.ip_address).exists()

        if banned:
            return HttpResponseForbidden('You are banned.')
        else:
            return None


class PublicVisitorMiddleware(object):
    """Middleware will log all IP addresses that access our public facing URLs."""

    def process_request(self, request):
        """
        The purpose of this middleware is to log every resource that was visted
        by an IP and keep a record.
        """
        # Save the visitor for the public view.
        request.visitor = PublicVisitor.objects.create(
            path=request.path,
            ip_address=request.ip_address
        )

        # Detect malicious intent.
        if request.visitor.is_path_suspicious():
            request.visitor.is_suspicious = True
            request.visitor.save()

        # Return nothing.
        return None  # Finish our middleware handler.


class PublicTrapURLMiddleware(object):
    def process_request(self, request):
        """Automatically ban IP's attempting to access suspicious URLs."""
        if request.path in constants.SUSPICIOUS_PATHS:
            try:
                BannedIP.objects.create(
                    address=request.ip_address,
                    reason=request.path
                )
            except Exception as e:
                pass
            return HttpResponseForbidden('You are banned.')
        else:
            return None  # Finish our middleware handler.
