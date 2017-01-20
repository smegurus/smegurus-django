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
from foundation_tenant.utils import int_or_none
from smegurus import constants


DOCXPRESSO_URL = "http://docxpresso.smegurus.com/tests/generateDoc.php"
DOCXPRESSO_PUBLIC_KEY = "" #TODO: Implement.
DOCXPRESSO_PRIVATE_KEY = "" #TODO: Implement.


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
        # - - - - - - - - - SECURITY INFO - - - - - - - - -
        # 1. You have to provide the user public key that is stored in the congig.ini file of the Docxpresso API Core (/opt/docxpresso/config.ini in our installation) .
        # 2. Generate the current timestamp (requests expire in 15 seconds).
        # 3. Generate the APIKEY. In order to do so you have to use HMAC: https://docs.python.org/2/library/hashlib.html beware with sha1 as hashing algorithm and no MD5 ...the key is the private key and the message is built concatenating the public key, private key and timestamp (the private key is also available in config.ini).
        # - - - - - - - - - - - - - - - - - - - - - - - - -

        import hashlib

        encoded_body = json.dumps({
        "security": {
            "publicKey": "da0d6f3ce2c47993e0e1a67f38cdb6b4b1d1fcbdca0d6f3ce2c47993e0e1a97a",
            "timestamp": 1483634192,
            "APIKEY": "df422fad370f8028510377d019f8d1a5e4c7e840"
        },
        "template": "templates/stage2.odt",
        "output": {
            "format": "odt",
            "response": "doc",
            "name": "testdoc"
        },
        "replace": [
            {
                "vars": [
                    {
                        "var": "workspace_name",
                        "value": "No-nonsense <span style='color:red'>Labs<\/span>"
                    },
                    {
                        "var": "naics_industry_name",
                        "value": "Information Technologies"
                    },
                    {
                        "var": "naics_industry_friendly_name",
                        "value": [
                                "Internet Apps"
                            ]
                        }
                    ]
                }
            ]
        })

        http = urllib3.PoolManager()

        r = http.request(
            'POST',
            DOCXPRESSO_URL,
            headers={'Content-Type': 'application/json'},
            body=encoded_body
        )
        print("\n")
        print(r.status)
        print(r.data)
        print(r.read())
        print("\n")


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
