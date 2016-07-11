from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class UserModelEmailBackend(ModelBackend):
    """Source: https://djangosnippets.org/snippets/10547/"""

    def authenticate(self, username="", password="", **kwargs):
        """Allow users to log in with their email address."""
        try:
            user = get_user_model().objects.get(email__iexact=username)
            if check_password(password, user.password):
                return user
            else:
                return None
        except get_user_model().DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None
