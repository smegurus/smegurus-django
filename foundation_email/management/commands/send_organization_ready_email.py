from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives    # EMAILER
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string    # HTML to TXT
from smegurus import constants
from foundation_public.models.organizationregistration import PublicOrganizationRegistration


class Command(BaseCommand):
    help = 'Command will send an email notifying the use that their organization has been built and is ready.'

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+')

    def handle(self, *args, **options):
        for registered_id in options['id']:
            # Fetch the User account associated with this email.
            try:
                organization = PublicOrganizationRegistration.objects.get(id=registered_id)
                if organization:
                    self.begin_processing(organization)
            except User.DoesNotExist:
                pass

    def begin_processing(self, organization):
        # Generate the data.
        subject = "Organization Ready"
        param = {
            'organization': organization,
            'constants': constants
        }

        # Plug-in the data into our templates and render the data.
        text_content = render_to_string('foundation_auth/org_ready.txt', param)
        html_content = render_to_string('foundation_auth/org_ready.html', param)

        # Generate our address.
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [organization.owner.email]

        # Send the email.
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
