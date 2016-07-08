from django.core.signing import Signer
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from foundation_public import constants
from foundation_public.models.organization import PublicOrganization
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

        # Variables used to generate your output.
        url = 'http://smegurus.xyz/en/activate/' + value + '/'
        subject_text = _('Account Activation')
        html_text = _('Click the following link to activate your account: %(url)s') % {'url': str(url)}

        # Get the specific groups we will filter by.
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)

        # Generate the message of the email and include the signed value
        # along with the URL to go to to activate the user for the specific
        # group User type.
        if entrepreneur_group in user.groups.all():
            subject_text = _('Account Activation - SME Gurus')
            html_text = _('Thank you for signing up your organization for SME Gurus! Please click the following link to validate your account.\n\n %(url)s \n\n If you believe you have received this message in error, please contact support@smegurus.com\n\nThank you!') % {'url': str(url)}
        if org_admin_group in user.groups.all():
            subject_text = _('Account Activation - SME Gurus for your Organization')
            html_text = _('Thank you for signing up your SME Gurus account! Please click the following link to validate your account.\n\n %(url)s \n\n If you believe you have received this message in error, please contact support@smegurus.com \n\n Thank you!') % {'url': str(url)}

        # Debugging purposes only.
        # print(html_text)

        # Send the email.
        send_mail(
            subject_text,
            html_text,
            env_var('DEFAULT_FROM_EMAIL'),
            [user.email],
            fail_silently=False
        )
