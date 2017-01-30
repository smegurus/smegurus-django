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

    def get_docxpresso_data(self, workspace, document, answers):
        docxpresso_data = []
        for answer in answers.all():
            if answer.question.pk == 21: # workspace_name
                docxpresso_data = self.do_q21(docxpresso_data, answer)

        # DEBUGGING PURPOSES
        print(docxpresso_data)

        return docxpresso_data # Return our data.

    def do_q21(self, docxpresso_data, answer):
        docxpresso_data.append({
            "vars": [{
                "var": "workspace_name",
                "value": answer.content['var_1']
            }]
        })
        return docxpresso_data
