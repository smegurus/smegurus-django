from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from foundation_public.models.me import PublicMe


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Source:
# http://stackoverflow.com/questions/14838128/django-rest-framework-token-authentication


# This code will create the profile model for whenever a new User has been created.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_me(sender, instance=None, created=False, **kwargs):
    if created and instance:
        PublicMe.objects.create(
            name=instance.first_name+' '+instance.last_name,
            owner=instance,
        )
