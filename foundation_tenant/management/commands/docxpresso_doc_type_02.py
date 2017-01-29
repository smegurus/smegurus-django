import json
import urllib3  # Third Party Library
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from django.core.management import call_command
from foundation_tenant.models.bizmula.documenttype import DocumentType
from foundation_tenant.models.bizmula.question import Question
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.slide import Slide
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer
from foundation_tenant.models.base.me import TenantMe
from foundation_tenant.models.base.fileupload import TenantFileUpload
from foundation_tenant.models.base.naicsoption import NAICSOption
from foundation_tenant.utils import int_or_none
from smegurus import constants


# Library used for the SHA1 hash algorithm.
from passlib.hash import sha1_crypt
from django.utils import timezone  # Timezone.
from datetime import datetime, timedelta  # Datetime.


class Command(BaseCommand):
    help = _('Docxpresso processing command for the particular document in a tenant.')

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+')

    def handle(self, *args, **options):
        """
        Function will get the inputted tenant name and doc_id and
        set the database to the tenant schema and begin processing
        for the particular document.
        """
        schema_name = options['id'][0]
        doc_id = int_or_none(options['id'][1])

        # the tenant metadata is stored.
        from django.db import connection

        # Connection will set it back to our tenant.
        connection.set_schema(schema_name, True) # Switch to Tenant.

        try:
            doc = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            raise CommandError(_('Cannot find a document.'))
        except Exception as e:
            raise CommandError(_('Unknown error occured.'))

        # Take our document and submit the answers to Docxpresso.
        self.begin_processing(doc)

        # Take our document and email.
        self.finalize_processing(doc)

    def begin_processing(self, document):
        """
        Function will load up all the answers for the particular document
        and submit it to Docxpresso.
        """
        # Generate timestamp.
        stem = "doc_" + str(document.id)
        suffix = "odt"
        filename = stem + '.' + suffix
        current = datetime.now()
        timestamp = str(current.strftime('%Y%m%d%H%M%S'))

        # Generate our API key.
        api_key = settings.DOCXPRESSO_PUBLIC_KEY + settings.DOCXPRESSO_PRIVATE_KEY + str(timestamp)
        api_key_hashed = sha1_crypt.hash(api_key) #  (Deprecated: https://passlib.readthedocs.io/en/stable/lib/passlib.hash.sha1_crypt.html)

        # Generate our Docxpresso data to submit.
        docxpresso_data = self.generate_docxpresso_data(document)

        # Generate our API call - Genere using Python dictonary.
        data = {
            "security": {
                "publicKey": settings.DOCXPRESSO_PUBLIC_KEY,
                "timestamp": timestamp,
                "APIKEY": api_key_hashed
            },
            "template": "templates/stage2.odt",
            "output": {
                "format": suffix,
                "response": "doc",
                "name": stem
            },
            "replace": [
                {
                    "vars": docxpresso_data
                }
            ]
        }

        # We will convert our Python dictonary into a JSON diconary.
        encoded_body = json.dumps(data).encode('utf-8')

        # Send AJAX Post to Docxpresso server.
        http = urllib3.PoolManager()
        r = http.request(
            'POST',
            settings.DOCXPRESSO_URL,
            # body=encoded_body,
            fields={
                "dataJSON": encoded_body
            }
            # headers={'Content-Type': 'application/json'}
        )

        doc_file = open('static/'+filename, 'wb')
        doc_file.write(r.data)
        doc_file.close()

        # Open the saved file and create a file object associated with it
        # and attach it to the document which will cause our file to be
        # uploaded to the S3 instance.
        from django.core.files import File
        with open('static/'+filename, 'rb') as f:
            # If the file already exists then delete it from S3.
            if document.docxpresso_file:
                document.docxpresso_file.delete()

            # Generate our new file.
            document.docxpresso_file = TenantFileUpload.objects.create(
                datafile = File(f),
            )
            document.save()

            # Delete the local file.
            #TODO: Implement this.

        # Return a success message to the console.
        self.stdout.write(
            self.style.SUCCESS(_('Finished importing Document #%s.') % str(document.id))
        )

    def generate_docxpresso_data(self, document):
        docxpresso_data = []
        answers = QuestionAnswer.objects.filter(document=document)
        for answer in answers.all():
            if answer.question.pk == 21: # workspace_name
                docxpresso_data.append({
                    "var": "workspace_name",
                    "value": answer.content['var_1']
                })

            if answer.question.pk == 25: # naics_industry_name
                naics_id = answer.content['var_5'] # Depth 5 NAICS ID
                depth_five_naics = NAICSOption.objects.get(id=naics_id) # Get the name

                docxpresso_data.append({
                    "var": "naics_industry_name",
                    "value": depth_five_naics.name
                })
                docxpresso_data.append({
                    "var": "naics_industry_friendly_name",
                    "value": answer.content['var_6']
                })

            if answer.question.pk == 26: # years_of_exp
                docxpresso_data.append({
                    "var": "years_of_exp",
                    "value": answer.content['var_1']
                })

            if answer.question.pk == 27: # business_idea
                docxpresso_data.append({
                    "var": "business_idea",
                    "value": answer.content['var_1']
                })

            if answer.question.pk == 28: # research_sources
                arr = []
                if answer.content['var_1_other']:
                    arr.append(answer.content['var_1_other'])
                else:
                    if answer.content['var_1']:
                        arr.append(answer.content['var_1'])

                if answer.content['var_2_other']:
                    arr.append(answer.content['var_2_other'])
                else:
                    if answer.content['var_2']:
                        arr.append(answer.content['var_2'])

                if answer.content['var_3_other']:
                    arr.append(answer.content['var_3_other'])
                else:
                    if answer.content['var_3']:
                        arr.append(answer.content['var_3'])

                if answer.content['var_4_other']:
                    arr.append(answer.content['var_4_other'])
                else:
                    if answer.content['var_4']:
                        arr.append(answer.content['var_4'])

                if answer.content['var_5_other']:
                    arr.append(answer.content['var_5_other'])
                else:
                    if answer.content['var_5']:
                        arr.append(answer.content['var_5'])

                docxpresso_data.append({
                    "var": "research_sources",
                    "value": arr
                })

            if answer.question.pk == 29: # similar_businesses
                arr = []
                arr.append(answer.content['var_1'])
                arr.append(answer.content['var_2'])
                arr.append(answer.content['var_3'])
                docxpresso_data.append({
                    "var": "similar_businesses",
                    "value": arr
                })

            if answer.question.pk == 30: # industry_contacts
                arr = []
                arr.append(answer.content['var_1'])
                arr.append(answer.content['var_2'])
                arr.append(answer.content['var_3'])
                docxpresso_data.append({
                    "var": "industry_contacts",
                    "value": arr
                })

        return docxpresso_data

    def finalize_processing(self, document):
        pass
