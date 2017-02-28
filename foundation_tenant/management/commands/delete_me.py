import os
import sys
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection # Used for django tenants.
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.me import Me


class Command(BaseCommand):
    help = _('Delete me in tenant.')

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+')

    def handle(self, *args, **options):
        schema_name = options['id'][0]
        email = int_or_none(options['id'][1])

        # Connection will set it back to our tenant.
        connection.set_schema(schema_name, True) # Switch to Tenant.

        try:
            me = Me.objects.get(owner__email=email)
            me.delete()
            self.stdout.write(
                self.style.SUCCESS(_('Successfully deleted me.'))
            )
        except Me.DoesNotExist:
            raise CommandError(_('Me doest not exist at specificed email'))
