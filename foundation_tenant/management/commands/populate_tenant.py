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
from foundation_tenant.models.base.me import TenantMe
from foundation_tenant.models.base.countryoption import CountryOption
from foundation_tenant.models.base.provinceoption import ProvinceOption
from foundation_tenant.models.base.cityoption import CityOption
from smegurus.settings import env_var


# NOTE:
# To run this from console, enter:
# python manage.py tenant_command populate_tenant


class Command(BaseCommand):
    help = _('Populates various data for the tenant.')

    def handle(self, *args, **options):
        # The filename of all the objects to be imported.
        ordered_file_names = [
            'countryoption.json',
            'provinceoption.json',
            'cityoption.json',
            'governmentbenefitoption.json',
            'identifyoption.json',
            'inforesourcecategory.json',
            'documenttype.json',
            'module_01.json',
            'module_02.json',
            'module_03.json',
            'module_04.json',
            'module_05.json',
            'module_06.json',
            'module_07.json',
            'module_08.json',
            'slide_01.json',
            'slide_02.json',
            'slide_03.json',
            'slide_04.json',
            'slide_05.json',
            'slide_06.json',
            'slide_07.json',
            'slide_08.json',
            'question_01.json',
            'question_02.json',
            'question_03.json',
            'question_04.json',
            'question_05.json',
            'question_06.json',
            'question_07.json',
            'question_08.json',
            'notification.json'
        ]

        # Iterate through all the filenames and load them into database.
        for file_name in ordered_file_names:
            call_command('loaddata', file_name, verbosity=0, interactive=False)
