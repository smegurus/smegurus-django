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
            self.style.SUCCESS(_('Finished processing stage 1 for workspace_id #%s.') % str(workspace_id))
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
                document_type__stage_num=1
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
                document__document_type__stage_num=1
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
            name="workspace_" + str(workspace.id) + "_stage_01",
            format="odt",
            template="templates/stage1.odt"
        )

        # Take our stage 2 content and populate docxpresso with it.
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
        for answer in answers.all():
            if answer.question.pk == 1:
                self.do_q1(answer, api)

            elif answer.question.pk == 2:
                self.do_q2(answer, api)

            elif answer.question.pk == 3:
                self.do_q3(answer, api)

            elif answer.question.pk == 4:
                self.do_q4(answer, api)

            elif answer.question.pk == 5:
                self.do_q5(answer, api)

            elif answer.question.pk == 6:
                self.do_q6(answer, api)

            if answer.question.pk == 7:
                self.do_q7(answer, api)

            if answer.question.pk == 8:
                self.do_q8(answer, api)

            if answer.question.pk == 9:
                self.do_q9(answer, api)

            if answer.question.pk == 10:
                self.do_q10(answer, api)

    def do_q1(self, answer, api):
        api.add_text("self_assess_1", answer.content['var_1'])

    def do_q2(self, answer, api):
        api.add_text("self_assess_2", answer.content['var_1'])

    def do_q3(self, answer, api):
        api.add_text("self_assess_3", answer.content['var_1'])

    def do_q4(self, answer, api):
        api.add_text("self_assess_4", answer.content['var_1'])

    def do_q5(self, answer, api):
        api.add_text("self_assess_5", answer.content['var_1'])

    def do_q6(self, answer, api):
        api.add_text("self_assess_6", answer.content['var_1'])

    def do_q7(self, answer, api):
        api.add_text("self_assess_7", answer.content['var_1'])

    def do_q8(self, answer, api):
        api.add_text("self_assess_8", answer.content['var_1'])

    def do_q9(self, answer, api):
        api.add_text("self_assess_9", answer.content['var_1'])

    def do_q10(self, answer, api):
        api.add_text("self_assess_10", answer.content['var_1'])
