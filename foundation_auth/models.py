from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.management import call_command


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_and_send_public_activation_email(sender, instance=None, created=False, **kwargs):
    """
    When the User account gets created, this function will be run which will
    send and email to the user account.
    """
    if created:
        call_command('send_public_activation_email',str(instance.email))

# Source:
# http://stackoverflow.com/questions/14838128/django-rest-framework-token-authentication
