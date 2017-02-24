import os
import sys
from decimal import *
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import connection # Used for django tenants.
from django.db.models import Sum
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.core.management import call_command
from smegurus import constants
from foundation_public.models.organization import PublicOrganization

from smegurus.settings import env_var


# NOTE:
# To run this from console, enter:
# python manage.py tenant_command populate_tenant


class Command(BaseCommand):
    help = _('Iterates through all tenants in system and updates our system data.')

    def handle(self, *args, **options):
        connection.set_schema_to_public() # Switch to Public.

        # Fetch all the tenants.
        tenants = PublicOrganization.objects.all()
        for tenant in tenants.all():
            # Load the tenant schema.
            tenant.load_schema()

            # Run populate_tenant on tenant to get latest data.
            call_command('populate_tenant')

        self.stdout.write(
            self.style.SUCCESS(_('Successfully populated tenant.'))
        )
