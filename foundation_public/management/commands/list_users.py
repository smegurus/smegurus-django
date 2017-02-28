import os
import sys
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection # Used for django tenants.
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = _('Activates a user.')

    def handle(self, *args, **options):
        # Connection needs first to be at the public schema, as this is where
        # the database needs to be set before listing.
        connection.set_schema_to_public() # Switch to Public.

        users = User.objects.all()
        for user in users.all():
            group_names = ""
            for group in user.groups.all():
                group_names += str(group)+", "
            self.stdout.write(
                self.style.SUCCESS("ID "+str(user.id)+" - "+user.get_full_name()+" - "+user.email+" - "+group_names)
            )
