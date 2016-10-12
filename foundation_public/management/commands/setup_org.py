import os
import sys
from decimal import *
from django.db.models import Sum
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.core.management import call_command
from foundation_public.models.organization import PublicOrganization
from smegurus import settings


class Command(BaseCommand):
    help = _('Loads all the data necessary to operate this application.')

    def handle(self, *args, **options):
        #create your public tenant
        public_tenant = PublicOrganization(
            domain_url=settings.SMEGURUS_APP_DOMAIN,
            schema_name='public',
            name='SMEGurus',
            paid_until='2016-12-05',
            on_trial=False,
            has_perks=False,
            has_mentors=False,
            how_many_served=1,
        )
        try:
            print("Creating Public")
            public_tenant.save()
        except Exception as e:
            print(e)

        # First tenant.
        tenant = PublicOrganization(
            domain_url='demo.'+str(settings.SMEGURUS_APP_DOMAIN),
            schema_name='demo',
            name='SMEGurus Demo',
            paid_until='2016-12-05',
            on_trial=True,
            has_perks=False,
            has_mentors=False,
            how_many_served=1,
        )
        try:
            print("Creating Tenant")
            tenant.save() # migrate_schemas automatically called, your tenant is ready to be used!
        except Exception as e:
            print(e)
