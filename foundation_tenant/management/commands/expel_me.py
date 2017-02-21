import os
import sys
from decimal import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import Sum
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.core.management import call_command
from smegurus import constants
from foundation_tenant.models.base.me import Me
from smegurus.settings import env_var


class Command(BaseCommand):
    help = _('Expel User in an Organization')

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+')

    def handle(self, *args, **options):
        for me_id in options['id']:
            try:
                me = Me.objects.get(id=me_id)
                for group in me.owner.groups.all():
                    if group.id in constants.MANAGEMENT_EMPLOYEE_GROUP_IDS:
                        self.begin_processing(me)
            except Me.DoesNotExist:
                pass

    def begin_processing(self, me):
        #-----------------------------#
        # Expel our User.             #
        #-----------------------------#
        me.is_in_intake = False
        me.save()

        #-----------------------------#
        # Send a notification email.  #
        #-----------------------------#
        # Variables used to generate your output.
        url = settings.SMEGURUS_APP_HTTP_PROTOCOL + '%s' % settings.SMEGURUS_APP_HTTP_DOMAIN + '/en/login/'
        subject_text = 'You are enrolled!'
        html_text = _('Congradulations you have been enrolled! Click the link to get started: %(url)s') % {'url': str(url)}

        # Send the email.
        send_mail(
            subject_text,
            html_text,
            env_var('DEFAULT_FROM_EMAIL'),
            [me.owner.email],
            fail_silently=False
        )
