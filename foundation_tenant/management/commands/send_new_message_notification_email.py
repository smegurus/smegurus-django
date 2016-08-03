from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.message import Message
from foundation_tenant.models.me import TenantMe
from foundation_public import constants
from smegurus.settings import env_var


class Command(BaseCommand):
    help = 'Command will send a new message was received for the inputted id.'

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+')

    def handle(self, *args, **options):
        for message_id in options['id']:
            # Fetch the User account associated with this email.
            try:
                message = Message.objects.get(id=int(message_id))
                self.begin_processing(message)
            except Message.DoesNotExist:
                pass

    def begin_processing(self, message):
        # Variables used to generate your output.
        http_protocol = 'https://' if env_var("SECURE_SSL_REDIRECT") else 'http://'
        url = http_protocol + '%s' % Site.objects.get_current().domain
        url += reverse('foundation_auth_user_login')
        url = url.replace("None","en")
        subject_text = 'New Message'
        html_text = _('You have received a new message. Please login to SME Gurus here to read it: %(url)s') % {'url': str(url)}

        send_mail(  # Send the email.
            subject_text,
            html_text,
            env_var('DEFAULT_FROM_EMAIL'),
            [message.recipient.owner.email,],
            fail_silently=False
        )
