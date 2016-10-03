from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class SMEGurusIPAddressMiddleware(object):
    def process_request(self, request):
        """
        The purpose of this middleware is to attach an IP to our requests.
        Source: http://stackoverflow.com/a/4581997
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = None
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.ip_address = ip
        return None


class SMEGurusAuthTokenMiddleware(object):
    def process_request(self, request):
        """
            The purpose of this middleware is to attach a 'token' variable
            to the request if the User has been logged in and if a Token does not
            exist then create one.
        """
        if request.user.is_authenticated():
            try:
                request.token = Token.objects.get(user_id=request.user.id)
            except Token.DoesNotExist:
                request.token = Token.objects.create(user_id=request.user.id)
        return None
