import os
import sys
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection # Used for django tenants.
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.organization import PublicOrganization


class Command(BaseCommand):
    help = _('Creates a tenant for the inputted organization registration id.')

    def add_arguments(self, parser):
        parser.add_argument('schema_name', nargs='+')

    def handle(self, *args, **options):
        # Connection needs first to be at the public schema, as this is where
        # the database needs to be set before creating a new tenant. If this is
        # not done then django-tenants will raise a "Can't create tenant outside
        # the public schema." error.
        connection.set_schema_to_public()

        # Fetch our registered Organization.
        for schema_name in options['schema_name']:
            try:
                # Fetch the organization.
                organization = PublicOrganization.objects.get(schema_name__iexact=schema_name)

                # Delete all the users in that organization.
                # users = organization.users
                # for user in users.all():
                #     user.delete()

                # Delete the tenant.
                organization.delete()

                # Provide successful message.
                self.stdout.write(
                    self.style.SUCCESS(_('Successfully deleted organization.'))
                )
            except Exception as e:
                raise CommandError(_('Deleted organization has error: %s') % str(e))
