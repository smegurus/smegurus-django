import os
import sys
from decimal import *
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db.models import Sum
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.core.management import call_command
from smegurus import constants
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.country import Country
from smegurus.settings import env_var


# NOTE:
# To run this from console, enter:
# python manage.py --tenant=demo populate_tenant


class Command(BaseCommand):
    help = _('Populates various data for the tenant.')

    def handle(self, *args, **options):
        self.begin_processing()

    def begin_importing_countries(self):
        Country.objects.bulk_create([
            Country(id=10, name="Canada",),
            Country(id=11, name="United States",),
            Country(id=12, name="Mexico",),
        ])

    def begin_processing(self):
        self.begin_importing_countries()
