import json
import urllib3  # Third Party Library
from passlib.hash import sha1_crypt # Library used for the SHA1 hash algorithm.
from datetime import datetime, timedelta  # Datetime.
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone  # Timezone.
from django.core.management import call_command
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer
from foundation_tenant.models.base.fileupload import TenantFileUpload
from foundation_tenant.models.base.naicsoption import NAICSOption
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
        schema_name = options['id'][0]
        workspace_id = int_or_none(options['id'][1])

        # the tenant metadata is stored.
        from django.db import connection

        # Connection will set it back to our tenant.
        connection.set_schema(schema_name, True) # Switch to Tenant.

        self.begin_processing(workspace_id)

        # Return a success message to the console.
        self.stdout.write(
            self.style.SUCCESS(_('Finished processing stage 3 for workspace_id #%s.') % str(workspace_id))
        )

    def get_workspace(self, workspace_id):
        """
        Utility function will return the Workspace for the parameter ID.
        """
        try:
            return Workspace.objects.get(id=workspace_id)
        except Workspace.DoesNotExist:
            raise CommandError(_('Cannot find a workspace.'))
        except Exception as e:
            raise CommandError(_('Unknown error occured: %s.' % e))

    def get_document(self, workspace_id):
        try:
            return Document.objects.get(
                workspace_id=workspace_id,
                document_type__stage_num=3
            )
        except Workspace.DoesNotExist:
            raise CommandError(_('Cannot find a workspace.'))
        except Exception as e:
            raise CommandError(_('Unknown error occured: %s.' % e))

    def get_answers(self, workspace_id):
        """
        Utility function will return all answers for the parameter workspace ID.
        """
        return QuestionAnswer.objects.filter(
            Q(
                workspace_id=workspace_id,
                document__document_type__stage_num=2
            ) | Q(
                workspace_id=workspace_id,
                document__document_type__stage_num=3
            )
        )

    def begin_processing(self, workspace_id):
        workspace = self.get_workspace(workspace_id)
        document = self.get_document(workspace_id)
        answers = self.get_answers(workspace_id)
        self.process(workspace, document, answers)

    def process(self, workspace, document, answers):
        # DEBUGGING PURPOSES
        # for answer in answers.all():
        #     print(answer.question.id, answer)

        # Generate timestamp.
        stem = "workspace_" + str(workspace.id) + "_stage_03"
        suffix = "odt"
        filename = stem + '.' + suffix
        current = datetime.now()
        timestamp = str(current.strftime('%Y%m%d%H%M%S'))

        # Generate our API key.
        api_key = settings.DOCXPRESSO_PUBLIC_KEY + settings.DOCXPRESSO_PRIVATE_KEY + str(timestamp)
        api_key_hashed = sha1_crypt.hash(api_key) #  (Deprecated: https://passlib.readthedocs.io/en/stable/lib/passlib.hash.sha1_crypt.html)

        # Generate our Docxpresso data to submit.
        docxpresso_data = self.get_docxpresso_data(workspace, document, answers)

        data = {
            "security": {
                "publicKey": settings.DOCXPRESSO_PUBLIC_KEY,
                "timestamp": timestamp,
                "APIKEY": api_key_hashed
            },
            "template": "templates/stage3.odt",
            "output": {
                "format": suffix,
                "response": "doc",
                "name": stem
            },
            "replace": docxpresso_data
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
            # Create a new file upload and upload the data to a S3 instance.
            docxpresso_file = TenantFileUpload.objects.create(
                datafile = File(f),
            )

            # Fetch the document and then atomically modify it.
            with transaction.atomic():
                # Fetch the document.
                document = self.get_document(workspace.id)

                # If the file already exists then delete it from S3.
                if document.docxpresso_file:
                    document.docxpresso_file.delete()

                # Generate our new file.
                document.docxpresso_file = docxpresso_file
                document.save()

                # Delete the local file.
                #TODO: Implement this.

    def get_docxpresso_data(self, workspace, document, answers):
        docxpresso_data = []
        for answer in answers.all():
            if answer.question.pk == 21: # business_name
                docxpresso_data = self.do_q21(docxpresso_data, answer)

            if answer.question.pk == 25: # naics_industry_friendly_name
                docxpresso_data = self.do_q25(docxpresso_data, answer)

            elif answer.question.pk == 27: # business_idea
                docxpresso_data = self.do_q27(docxpresso_data, answer)

            elif answer.question.pk == 28: # research_sources
                docxpresso_data = self.do_q28(docxpresso_data, answer)

            elif answer.question.pk == 32: # product_categories
                docxpresso_data = self.do_q32(docxpresso_data, answer)

            elif answer.question.pk == 33: # customer_type
                docxpresso_data = self.do_q33(docxpresso_data, answer)

            elif answer.question.pk == 34: # business_oppportunity
                docxpresso_data = self.do_q34(docxpresso_data, answer)

            elif answer.question.pk == 35: # not_being_done_because
                docxpresso_data = self.do_q35(docxpresso_data, answer)

            elif answer.question.pk == 36: # business_solution
                docxpresso_data = self.do_q36(docxpresso_data, answer)

            elif answer.question.pk == 37: # pestel_trends
                docxpresso_data = self.do_q37(docxpresso_data, answer)

            elif answer.question.pk == 38: # specific_sources
                docxpresso_data = self.do_q38(docxpresso_data, answer)

            elif answer.question.pk == 39: # geographic_market
                docxpresso_data = self.do_q39(docxpresso_data, answer)

            elif answer.question.pk == 40: # geographic_market | customer_buying_decision
                docxpresso_data = self.do_q40(docxpresso_data, answer)

            elif answer.question.pk == 74: # how_to_convince
                docxpresso_data = self.do_q74(docxpresso_data, answer)

            # customers_will_purchase ??
            # product_distribution ???
            # target_market_characteristics 49

        return docxpresso_data # Return our data.

    def do_q21(self, docxpresso_data, answer):
        docxpresso_data.append({
            "vars": [{
                "var": "business_name",
                "value": answer.content['var_1']
            }]
        })
        return docxpresso_data

    def do_q25(self, docxpresso_data, answer):
        docxpresso_data.append({
            "vars": [{
                "var": "naics_industry_friendly_name",
                "value": answer.content['var_6']
            }]
        })
        return docxpresso_data

    def do_q27(self, docxpresso_data, answer):
        docxpresso_data.append({
            "vars": [{
                "var": "business_idea",
                "value": answer.content['var_1']
            }]
        })
        return docxpresso_data

    def do_q28(self, docxpresso_data, answer):
        arr = []
        arr.append(answer.content['var_1'])
        arr.append(answer.content['var_2'])
        arr.append(answer.content['var_3'])
        docxpresso_data.append({
            "vars": [{
                "var": "research_sources",
                "value": arr
            }],
            "options": {
                "element": "list"
            }
        })
        return docxpresso_data

    def do_q32(self, docxpresso_data, answer):
        arr = []
        arr.append(answer.content['var_1'])
        arr.append(answer.content['var_2'])
        arr.append(answer.content['var_3'])
        docxpresso_data.append({
            "vars": [{
                "var": "product_categories",
                "value": arr
            }],
            "options": {
                "element": "list"
            }
        })
        return docxpresso_data

    def do_q33(self, docxpresso_data, answer):
        docxpresso_data.append({
            "vars": [{
                "var": "customer_type",
                "value": answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
            }]
        })
        return docxpresso_data

    def do_q34(self, docxpresso_data, answer):
        docxpresso_data.append({
            "vars": [{
                "var": "business_oppportunity",
                "value": answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
            }]
        })
        return docxpresso_data

    def do_q35(self, docxpresso_data, answer):
        docxpresso_data.append({
            "vars": [{
                "var": "not_being_done_because",
                "value": answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
            }]
        })
        return docxpresso_data

    def do_q36(self, docxpresso_data, answer):
        docxpresso_data.append({
            "vars": [{
                "var": "business_solution",
                "value": answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
            }]
        })
        return docxpresso_data

    def do_q37(self, docxpresso_data, answer):
        # Get all our trends.
        arr = []
        for ans in answer.content:
            arr.append(ans['var_3'])

        # Generate our data and return it.
        docxpresso_data.append({
            "vars": [{
                "var": "pestel_trends",
                "value": arr
            }]
        })
        return docxpresso_data

    def do_q38(self, docxpresso_data, answer):
        # Get all our trends.
        arr = []
        for ans in answer.content:
            arr.append(ans['var_2'])

        # Generate our data and return it.
        docxpresso_data.append({
            "vars": [{
                "var": "specific_sources",
                "value": arr
            }]
        })
        return docxpresso_data

    def do_q39(self, docxpresso_data, answer):
        docxpresso_data.append({
            "vars": [{
                "var": "geographic_market",
                "value": answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
            }]
        })
        return docxpresso_data

    def do_q40(self, docxpresso_data, answer): # customer_buying_decision | geographic_market
        # Compute the answer.
        var_1 = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']

        # Add our result.
        docxpresso_data.append({
            "vars": [{
                "var": "customer_buying_decision",
                "value": '-' if answer.content['var_0'] else var_1
            }]
        })
        return docxpresso_data

    def do_q74(self, docxpresso_data, answer): #TODO Imp
        # Get all our trends.
        arr = []
        for ans in answer.content['var_1']:
            arr.append(ans['value'])

        # Generate our data and return it.
        docxpresso_data.append({
            "vars": [{
                "var": "how_to_convince",
                "value": arr
            }]
        })
        return docxpresso_data
