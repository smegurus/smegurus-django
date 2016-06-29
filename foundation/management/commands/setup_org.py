import os
import sys
from decimal import *
from django.db.models import Sum
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.core.management import call_command
from foundation.models.organization import Organization
from foundation.models.organization import Domain
from smegurus.settings import env_var


class Command(BaseCommand):
    help = _('Loads all the data necessary to operate this application.')

    def handle(self, *args, **options):
        #create your public tenant
        public_tenant = Organization(
            schema_name='public',
            name='SMEGurus',
            paid_until='2016-12-05',
            on_trial=False
        )
        try:
            print("Creating Public")
            public_tenant.save()
        except Exception as e:
            print(e)

        # Add one or more domains for the tenant
        domain = Domain()
        domain.domain = 'smegurus.xyz' # don't add your port or www here! on a local server you'll want to use localhost here
        domain.tenant = public_tenant
        domain.is_primary = True
        try:
            print("Creating Public Domain")
            domain.save()
        except Exception as e:
            print(e)

        # First tenant.
        tenant = Organization(
            schema_name='demo',
            name='SMEGurus Demo',
            paid_until='2016-12-05',
            on_trial=True
        )
        try:
            print("Creating Tenant")
            tenant.save() # migrate_schemas automatically called, your tenant is ready to be used!
        except Exception as e:
            print(e)

        # Add one or more domains for the tenant
        domain = Domain()
        domain.domain = 'demo.smegurus.xyz' # don't add your port or www here!
        domain.tenant = tenant
        domain.is_primary = True
        try:
            print("Creating Tenant Domain")
            domain.save()
        except Exception as e:
            print(e)
