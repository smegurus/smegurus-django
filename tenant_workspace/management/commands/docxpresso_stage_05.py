import os.path
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
from foundation_tenant.models.base.fileupload import FileUpload
from foundation_tenant.models.base.naicsoption import NAICSOption
from foundation_tenant.models.base.s3file import S3File
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
            self.style.SUCCESS(_('Finished processing stage 5 for workspace_id #%s.') % str(workspace_id))
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
                document_type__stage_num=5
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
                document__document_type__stage_num=3
            ) |
            Q(
                workspace_id=workspace_id,
                document__document_type__stage_num=5
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
            name="workspace_" + str(workspace.id) + "_stage_05",
            format="odt",
            template="templates/stage5.odt"
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
                # Try deleting the previously uploaded file and if the file
                # does not exist or ANY error occurs then catch it here and
                # safely continue our application.
                try:
                    document.docxpresso_file.delete()
                except Exception as e:
                    print("WARNING: ", str(e))

            # Save our file to DB.
            docxpresso_file = S3File.objects.create(
                stem=doc_filename,
                suffix='odt',
                owner=document.owner,
                key=doc_filename
            )
            docxpresso_file.upload_file(doc_bin_data)

            # Generate our new file.
            document.docxpresso_file = docxpresso_file
            document.save()

    def set_answers(self, answers, api):
        for answer in answers.all():
            if answer.question.pk == 36: # business_solution
                self.do_q36(answer, api)

            elif answer.question.pk == 51:
                self.do_q51(answer, api)

            elif answer.question.pk == 53:
                self.do_q53(answer, api)

            elif answer.question.pk == 54:
                self.do_q54(answer, api)

            elif answer.question.pk == 55:
                self.do_q55(answer, api)

            elif answer.question.pk == 73:
                self.do_q73(answer, api)

    def do_q36(self, answer, api):
        api.add_text(
            "business_solution",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q51(self, answer, api):
        api.add_text(
            "customer_price_sensitivity",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q54(self, answer, api):
        api.add_text(
            "test_reach_method",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q53(self, answer, api):
        api.add_text(
            "test_contact_number",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q55(self, answer, api):
        api.add_text(
            "test_contact_agreed",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q73(self, answer, api):
        array = []

        # Attach all the checkboxes.
        for ans in answer.content['var_1']:
            array.append(ans['value'])

        # Attach the other textfield.
        if answer.content['var_1_other']:
            array.append(answer.content['var_1_other'])

        # Attach our data to document.
        api.add_text_paragraphs("test_contact_method", array)
