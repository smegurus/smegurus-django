import os
import sys
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import connection # Used for django tenants.
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.organization import PublicOrganization


class Command(BaseCommand):
    help = _('Deletes tenant with schema name.')

    def add_arguments(self, parser):
        parser.add_argument('schema_name', nargs='+')

    def handle(self, *args, **options):
        # Connection needs first to be at the public schema, as this is where
        # the database needs to be set before deleting organization.
        connection.set_schema_to_public()

        # Fetch our registered Organization per "schema_name" and delete.
        for schema_name in options['schema_name']:
            try:
                organization = PublicOrganization.objects.get(schema_name__iexact=schema_name)
                organization.delete()
                self.stdout.write(
                    self.style.SUCCESS(_('Successfully deleted organization.'))
                )
            except Exception as e:
                raise CommandError(_('Deleted organization has error: %s') % str(e))
