from django.http import HttpResponseForbidden
from foundation_public.models.banned import BannedIP
from foundation_public.models.visitor import PublicVisitor


class PublicBanEnforcingMiddleware(object):
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


class PublicVisitorMiddleware(object):
    """Middleware will log all IP addresses that access our public facing URLs."""

    def get_client_ip(self, request):
        """Utility function for getting the IP. Source: http://stackoverflow.com/a/4581997"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def process_request(self, request):
        """
        The purpose of this middleware is to log every resource that was visted
        by an IP and keep a record.
        """
        # Save the visitor for the public view.
        request.visitor = PublicVisitor.objects.create(
            path=request.path,
            ip_address=self.get_client_ip(request)
        )

        # Detect malicious intent.
        if request.visitor.is_path_suspicious():
            request.visitor.is_suspicious = True
            request.visitor.save()

        # Return nothing.
        return None  # Finish our middleware handler.
