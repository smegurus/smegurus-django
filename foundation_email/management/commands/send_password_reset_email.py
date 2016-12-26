from django.core.signing import Signer
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from smegurus import constants
from smegurus.settings import env_var


class Command(BaseCommand):
    help = 'Command will send a password reset email for the inputted email.'

    def add_arguments(self, parser):
        parser.add_argument('email', nargs='+')

    def handle(self, *args, **options):
        for email in options['email']:
            # Fetch the User account associated with this email.
            try:
                user = User.objects.get(email=email)
                self.begin_processing(user)
            except User.DoesNotExist:
                pass

    def begin_processing(self, user):
        # Convert our User's ID into an encrypted value.
        # Note: https://docs.djangoproject.com/en/dev/topics/signing/
        signer = Signer()
        id_sting = str(user.id).encode()
        value = signer.sign(id_sting)

        # Variables used to generate your output.
        http_protocol = 'https://' if env_var("SECURE_SSL_REDIRECT") else 'http://'
        url = http_protocol + '%s' % Site.objects.get_current().domain + '/en/password_reset/' + value + '/'
        subject_text = 'Account Password Reset'
        html_text = _('Click the following link to reset your password: %(url)s') % {'url': str(url)}

        # Send the email.
        send_mail(
            subject_text,
            html_text,
            env_var('DEFAULT_FROM_EMAIL'),
            [user.email],
            fail_silently=False
        )
