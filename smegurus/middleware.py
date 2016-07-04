from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class SMEGurusTokenMiddleware(object):
    def process_request(self, request):
        """
            The purpose of this middleware is to attach a 'token' variable to
            the request if the User has been logged in and if a Token does not
            exist then create one.
        """
        if request.user.is_authenticated():
            try:
                request.token = Token.objects.get(user_id=request.user.id)
            except Token.DoesNotExist:
                request.token = Token.objects.create(user_id=request.user.id)

        return None  # Finish our middleware handler.
