import os
import sys
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection # Used for django tenants.
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = _('Creates a tenant for the inputted organization registration id.')

    def add_arguments(self, parser):
        parser.add_argument('email', nargs='+')

    def handle(self, *args, **options):
        # Connection needs first to be at the public schema, as this is where
        # the database needs to be set before creating a new tenant. If this is
        # not done then django-tenants will raise a "Can't create tenant outside
        # the public schema." error.
        connection.set_schema_to_public() # Switch to Public.

        # Fetch our registered Organization.
        for email in options['email']:
            try:
                user = User.objects.get(email=email)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(_('Successfully became root user.'))
                )
            except User.DoesNotExist:
                raise CommandError(_('user doest not exist at specificed email'))
