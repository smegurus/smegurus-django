import os
import sys
import csv
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.naicsoption import NAICSOption


# Constant stores how many characters the code needs to for the code to
# be considered a parent code.
BASE_PARENT_CODE_LENGTH = 2


class BIZNAICSOptionImporter:
    def __init__(self, file_path):
        self.file_path = file_path

    def begin_import(self):
        with open(self.file_path, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] != 'Seq. No.':  # Skip header row.
                    self.import_row(row)

    def create_niacs_option(self, seq_num, code, name, parent_id):
        #-------------------------------#
        # CASE 1 OF 2: HAS PARENT       #
        #-------------------------------#
        if parent_id:
            NAICSOption.objects.get_or_create(
                id=int(code),
                name=name,
                seq_num=int(seq_num),
                year=2012,
                parent_id=int(parent_id)
            )

        #-------------------------------#
        # CASE 2 OF 2: MISSING PARENT   #
        #-------------------------------#
        else:
            NAICSOption.objects.get_or_create(
                id=int(code),
                name=name,
                seq_num=int(seq_num),
                year=2012
            )

    def import_naics(self, seq_num, code, name):
        #-------------------------------#
        # CASE 1 OF 2: BASE PARENT      #
        #-------------------------------#
        if len(code) == BASE_PARENT_CODE_LENGTH:
            self.create_niacs_option(seq_num, code, name, None)

        #-------------------------------#
        # CASE 2 OF 2: NON-BASE PARENT  #
        #-------------------------------#
        else:
            parent_id = code[:-1]   # Strip the last character in the code.
            self.create_niacs_option(seq_num, code, name, parent_id)

    def import_row(self, row):
        # String variables to hold our NAICS option.
        seq_num = row[0]
        code = row[1]
        name = row[2]

        #-------------------------------#
        # CASE 1 OF 2: CODE HAS A RANGE #
        #-------------------------------#
        # Algorithm:
        # Split the code into start and end range and iterate throught
        # the range.
        if '-' in code:
            code_range = code.split("-")
            start = int(code_range[0])
            end = int(code_range[1])
            for i in range(start, end + 1):
                self.import_naics(seq_num, str(i), name)

        #--------------------------------#
        # CASE 2 OF 2: CODE HAS NO RANGE #
        #--------------------------------#
        else:
            self.import_naics(seq_num, code, name)


class Command(BaseCommand):
    """
        Run in your console:
        $ python manage.py tenant_command naics_import

    """
    help = 'ETL imports the NAICS options.'

    # DEPRECATED
    #-------------
    # def add_arguments(self, parser):
    #     parser.add_argument('file_path', nargs='+')

    def handle(self, *args, **options):
        # os.system('clear;')  # Clear the console text.

        # The following code will find the file path of our file in our app.
        import foundation_tenant
        app_path = os.path.dirname(foundation_tenant.__file__)
        file_path = app_path + "/static/naics_2012.csv"

        # Import all our data.
        importer = BIZNAICSOptionImporter(file_path)
        importer.begin_import()

        # DEPRECATED
        #-------------
        # for full_file_path in options['file_path']:
        #     importer = BIZNAICSOptionImporter(full_file_path)
        #     importer.begin_import()

        self.stdout.write(
            self.style.SUCCESS(_('Successfully imported NAICS.'))
        )


#-----------------
# DEVELOPER NOTES:
#-----------------
# Loading
#-----------
# Remember, if you want to load up a fixture from console, run:
# python manage.py loaddata all.json
#
# Exporting
#------------
# Export specific data from an application:
# python manage.py dumpdata --indent 4 --format=json foundation_tenant.NAICSOption > ~/Desktop/niacsoption.json
