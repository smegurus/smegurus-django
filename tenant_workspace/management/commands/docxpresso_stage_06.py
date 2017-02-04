import os.path
from django.utils import timezone
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
from foundation_tenant.docxpresso_utils import DocxspressoAPI
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

        api = DocxspressoAPI(
            settings.DOCXPRESSO_PUBLIC_KEY,
            settings.DOCXPRESSO_PRIVATE_KEY,
            settings.DOCXPRESSO_URL
        )

        self.begin_processing(workspace_id, api)

        # Return a success message to the console.
        self.stdout.write(
            self.style.SUCCESS(_('Finished processing stage 6 for workspace_id #%s.') % str(workspace_id))
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
                document_type__stage_num=6
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
            ) |
            Q(
                workspace_id=workspace_id,
                document__document_type__stage_num=6
            )
        )

    def begin_processing(self, workspace_id, api):
        workspace = self.get_workspace(workspace_id)
        answers = self.get_answers(workspace_id)
        self.process(workspace, answers, api)

    def process(self, workspace, answers, api):
        # DEBUGGING PURPOSES
        # for answer in answers.all():
        #     print(answer.question.id, answer)

        api.new(
            name="workspace_" + str(workspace.id) + "_stage_06",
            format="odt",
            template="templates/stage6.odt"
        )

        # Take our content and populate docxpresso with it.
        self.set_answers(answers, api)

        # Generate our document!
        doc_filename = api.get_filename()
        doc_bin_data = api.generate()

        # DEVELOPERS NOTE:
        # The following three lines will take the 'default_storage' class
        # django uses for saving files and apply it. Because we overloaded
        # this default class with S3 storage, therefore when this code runs
        # we will be saving to S3.
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile

        # Fetch the document and then atomically modify it.
        with transaction.atomic():
            # Fetch the document.
            document = self.get_document(workspace.id)

            # If the file already exists then delete it from S3.
            if document.docxpresso_file:
                document.docxpresso_file.delete()

            # Upload our file to S3 server.
            path = default_storage.save(
                'uploads/'+doc_filename,
                ContentFile(doc_bin_data)
            )

            # Save our file to DB.
            docxpresso_file = TenantFileUpload.objects.create(
                datafile = path,
            )

            # Generate our new file.
            document.docxpresso_file = docxpresso_file
            document.save()

    def set_answers(self, answers, api):
        today = timezone.now()
        api.add_text("date", str(today))

        for answer in answers.all():
            if answer.question.pk == 21:
                # workspace_name
                self.do_q21(answer, api)

            elif answer.question.pk == 56:
                # actual_contact_number
                self.do_q56(answer, api)

            elif answer.question.pk == 58:
                # actual_supported_number
                # validation_outcome_met
                self.do_q58(answer, api, answers)
            
            if answer.question.pk == 59:
                # validation_lessons_learned
                self.do_q59(answer, api)

    def do_q21(self, answer, api):
        api.add_text("workspace_name", answer.content['var_1'])
        api.add_text_to_footer("workspace_name", answer.content['var_1'])

    def do_q56(self, answer, api):
        api.add_text(
            "actual_contact_number",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q58(self, q58_answer, api, answers):
        # Find the other answer to compare to.
        q56_value = 0
        for answer in answers.all():
            if answer.question.pk == 56:
                q56_value = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']

        # Find the other value.
        q58_value = q58_answer.content['var_1_other'] if q58_answer.content['var_1_other'] else q58_answer.content['var_1']

        # # Debugging purposes only.
        # print("QID56", q56_value)
        # print("QID58", q58_value)

        # Decision computation.
        value = "Yes" if q58_value >= q56_value else "No"

        # # Debugging purposes only.
        # print("QID58 >= QID56 is", value)

        # Record our decision.
        api.add_text("validation_outcome_met", value)

        # Record another value.
        api.add_text("actual_supported_number", q56_value)

    def do_q59(self, answer, api):
        api.add_text("validation_lessons_learned",answer.content['var_1'])
