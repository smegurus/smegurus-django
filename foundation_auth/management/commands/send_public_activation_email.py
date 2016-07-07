from django.core.signing import Signer
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from smegurus.settings import env_var


class Command(BaseCommand):
    help = 'Command will send an activation email for the inputted email.'

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

#         (for organizations):
#
# Subject - Account Activation - SME Gurus for your Organization
#
# Thank you for signing up your organization for SME Gurus! Please click the following link to validate your account.
#
# If you believe you have received this message in error, please contact support@smegurus.com
#
# Thank you!
#
# (for entrepreneurs):
#
# Subject - Account Activation - SME Gurus
#
# Thank you for signing up your SME Gurus account! Please click the following link to validate your account.
#
# If you believe you have received this message in error, please contact support@smegurus.com
#
# Thank you!

        # Generate the message of the email and include the signed value
        # along with the URL to go to to activate the user.
        html_text = 'Click the following link to activate your account: ';
        html_text += 'http://smegurus.xyz/en/activate/' + value + '/'

        # Debugging purposes only.
        # print(html_text)

        # Send the email.
        send_mail(
            _("Account Activation"),
            html_text,
            env_var('DEFAULT_FROM_EMAIL'),
            [user.email],
            fail_silently=False
        )
