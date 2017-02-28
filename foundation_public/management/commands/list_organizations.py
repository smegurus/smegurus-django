import os
import sys
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection # Used for django tenants.
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.organization import PublicOrganization


class Command(BaseCommand):
    help = _('List all organization in our system.')

    def handle(self, *args, **options):
        # Connection needs first to be at the public schema, as this is where
        # the database needs to be set before listing.
        connection.set_schema_to_public() # Switch to Public.

        orgs = PublicOrganization.objects.all()
        for org in orgs.all():

            self.stdout.write(
                self.style.SUCCESS("ID "+str(org.id)+" - "+org.schema_name)
            )
