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
from foundation_tenant.models.base.me import Me
from foundation_tenant.utils import int_or_none
from smegurus import constants


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
        tenant_name = options['id'][0]
        doc_id = int_or_none(options['id'][1])

        # the tenant metadata is stored.
        from django.db import connection

        # Connection will set it back to our tenant.
        connection.set_schema(tenant_name, True) # Switch to Tenant.

        try:
            doc = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            raise CommandError(_('Cannot find a document.'))
        except Exception as e:
            raise CommandError(_('Unknown error occured.'))

        # Take our document and submit the answers to Docxpresso.
        self.begin_processing(doc)


    def begin_processing(self, document):
        """
        Function will load up all the answers for the particular document
        and submit it to Docxpresso.
        """


        # Library used for the SHA1 hash algorithm.
        from passlib.hash import sha1_crypt
        from django.utils import timezone  # Timezone.
        from datetime import datetime, timedelta  # Datetime.

        # Generate timestamp.
        stem = "doc_" + str(document.id)
        suffix = "odt"
        filename = stem + '.' + suffix
        current = datetime.now()
        timestamp = str(current.strftime('%Y%m%d%H%M%S'))

        # Generate our API key.
        api_key = settings.DOCXPRESSO_PUBLIC_KEY + settings.DOCXPRESSO_PRIVATE_KEY + str(timestamp)
        api_key_hashed = sha1_crypt.hash(api_key) #  (Deprecated: https://passlib.readthedocs.io/en/stable/lib/passlib.hash.sha1_crypt.html)

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
                    "vars": [
                        {
                            "var": "workspace_name",
                            "value": "Mika Software"

                        },
                        {
                            "var": "business_idea",
                            "value": "Mika Software"
                        },
                        {
                            "var": "naics_industry_name",
                            "value": "Information Technologies"
                        },
                        {
                            "var": "naics_industry_friendly_name",
                            "value": "Internet Apps"
                        },
                        {
                            "var": "years_of_exp",
                            "value": 1
                        },
                        {
                            "var": "research_source",
                            "value": ["Test 1", "Test 2"]
                        },
                        {
                            "var": "similar_business",
                            "value": ["Test 1", "Test 2", "Test 3"]
                        },
                        {
                            "var": "industry_contact",
                            "value": ["Test 1", "Test 2", "Test 3", "Test 4"]
                        }
                    ]
                }
            ]
        }

        # We will convert our Python dictonary into a JSON diconary.
        encoded_body = json.dumps(data).encode('utf-8')

        # Debugging purposes only.
        # print("PUBLIC URL:", settings.DOCXPRESSO_URL)
        # print("PUBLIC KEY:", settings.DOCXPRESSO_PUBLIC_KEY)
        # print("PRIVATE KEY:", settings.DOCXPRESSO_PRIVATE_KEY)
        # print("TIMESTAMP:", timestamp)
        # print("API KEY:", api_key_hashed)
        # print("API CALL:", encoded_body)

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

        # var2 = json.loads(r.data.decode('utf-8'))['json']
        # print(var2)
        # print('\n\n')

        # Debugging purposes only.
        # print("\n")
        # print(r.status)
        # print(r.data)
        # print(r.read())
        # print("\n")
        # result = json.loads(r.data.decode('utf-8'))['json']
        # print(result)

        outFile = open('static/'+filename, 'wb')
        outFile.write(r.data)
        outFile.close()

        # # Implement when ready...
        # answers = QuestionAnswer.objects.filter(document=document)
        # for answer in answers.all():
        #     self.process_answer(answer)

        self.stdout.write(
            self.style.SUCCESS(_('Finished importing Document #%s.') % str(document.id))
        )

    def process_answer(self, answer):
        print(answer)
        print("\n\n")
