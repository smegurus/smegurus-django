from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from smegurus.settings import env_var
from smegurus import constants


def base_constants(request):
    """
    The purpose of this context processor is to attach all our constants
    to every request template.
    """
    return {
        'constants': constants,
    }


def ip(request):
    """
    The purpose of this context processor is to attach an IP to our requests.
    Source: http://stackoverflow.com/a/4581997
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return {
        'ip': ip,
    }

def auth_token(request):
    """
        The purpose of this context processor is to attach a 'token' variable
        to the request if the User has been logged in and if a Token does not
        exist then create one.
    """
    token = None
    if request.user.is_authenticated():
        try:
            token = Token.objects.get(user_id=request.user.id)
        except Token.DoesNotExist:
            token = Token.objects.create(user_id=request.user.id)
    return {
        'token': token,
    }
