from django.core.signing import Signer
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.intake import Intake
from smegurus.settings import env_var
from smegurus import constants


# NOTE: This call command is integrated with 'django-tenants' library and
#       as a result you will have to use 'tenant_command' in your call. Here
#       is an example of calling this function:
#       - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#       python manage.py tenant_command send_reviewed_email_for_intake 2
#       - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Command(BaseCommand):
    help = 'Command will send an email for the inputted intake.'

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+')

    def handle(self, *args, **options):
        for intake_id in options['id']:
            # Fetch the User account associated with this email.
            try:
                intake = Intake.objects.get(id=int(intake_id))
                self.begin_processing(intake)
            except Intake.DoesNotExist:
                pass

    def begin_processing(self, intake):
        """Function will generate the email based on whether the employee manually created the entrpreneur or not."""
        url = None
        subject_text = None
        html_text = None

        # Generate the URL depending on whether the User was created by the employee or not.
        if intake.is_employee_created:
            url = self.generate_password_reset_url(intake.me.owner)
        else:
            url = self.generate_login_url()

        # Generate the email message depending on the status of the intake.
        if intake.status == constants.APPROVED_STATUS:
            subject_text = 'Application Reviewed: Accepted'
            html_text = _('You have been accepted! Click the following link to begin: %(url)s') % {'url': str(url)}
        elif intake.status == constants.REJECTED_STATUS:
            subject_text = 'Application Reviewed: Rejected'
            html_text = _('You have been rejected! Click the following link to read the reason: %(url)s') % {'url': str(url)}

        # Send the email.
        send_mail(
            subject_text,
            html_text,
            env_var('DEFAULT_FROM_EMAIL'),
            [intake.me.owner.email],
            fail_silently=False
        )

    def generate_password_reset_url(self, user):
        # Convert our User's ID into an encrypted value.
        # Note: https://docs.djangoproject.com/en/dev/topics/signing/
        signer = Signer()
        id_sting = str(user.id).encode()
        value = signer.sign(id_sting)

        # Variables used to generate your output.
        http_protocol = 'https://' if env_var("SECURE_SSL_REDIRECT") else 'http://'
        return http_protocol + '%s' % Site.objects.get_current().domain + '/en/password_reset/' + value + '/'

    def generate_login_url(self):
        http_protocol = 'https://' if env_var("SECURE_SSL_REDIRECT") else 'http://'
        url = http_protocol + '%s' % Site.objects.get_current().domain
        url += reverse('foundation_auth_user_login')
        return url.replace("None","en")
