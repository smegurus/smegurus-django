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
from foundation_tenant.models.base.s3file import S3File
from foundation_tenant.bizmula_utils import BizmulaAPI
from foundation_tenant.utils import int_or_none
from foundation_tenant.utils import get_random_string
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

        api = BizmulaAPI(
            settings.DOCXPRESSO_PUBLIC_KEY,
            settings.DOCXPRESSO_PRIVATE_KEY,
            settings.DOCXPRESSO_URL
        )

        self.begin_processing(workspace_id, api)

        # Return a success message to the console.
        self.stdout.write(
            self.style.SUCCESS(_('Finished processing stage 9 for workspace_id #%s.') % str(workspace_id))
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
                document_type__stage_num=9
            )
        except Workspace.DoesNotExist:
            raise CommandError(_('Cannot find a workspace.'))
        except Exception as e:
            raise CommandError(_('Unknown error occured: %s.' % e))

    def get_answers(self, workspace_id):
        """
        Utility function will return all answers for the parameter workspace ID.
        """
        return QuestionAnswer.objects.filter(workspace_id=workspace_id)

    def begin_processing(self, workspace_id, api):
        workspace = self.get_workspace(workspace_id)
        answers = self.get_answers(workspace_id)
        self.process(workspace, answers, api)

    def process(self, workspace, answers, api):
        api.new(
            name="workspace_" + str(workspace.id) + "_stage_09",
            format="odt",
            template="templates/stage9.ods"
        )

        # Take our content and populate docxpresso with it.
        self.set_answers(workspace, answers, api)

        # Generate our document!
        doc_filename = api.get_filename()
        doc_modified_filename = settings.SMEGURUS_APP_DOCXPRESSO_FILE_PREFIX+doc_filename
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
                key=doc_modified_filename
            )
            docxpresso_file.upload_file(doc_bin_data)

            # Generate our new file.
            document.docxpresso_file = docxpresso_file
            document.save()

    def set_answers(self, workspace, answers, api):
        # Assign date.
        self.do_date(api)

        # Iterate through all the answers and transcode the business plan.
        for answer in answers.all():
            if answer.question.pk == 61:
                api.do_q61(answer, api)

            elif answer.question.pk == 101:
                api.do_q101(answer, api)

            elif answer.question.pk == 104:
                api.do_q104(answer, api)

            elif answer.question.pk == 106:
                api.do_q106(answer, api)

            elif answer.question.pk == 107:
                api.do_q107(answer, api)

            elif answer.question.pk == 109:
                api.do_q109(answer, api)

            elif answer.question.pk == 110:
                api.do_q110(answer, api)

            elif answer.question.pk == 111:
                api.do_q111(answer, api)

            elif answer.question.pk == 113:
                api.do_q113(answer, api)

            elif answer.question.pk == 115:
                api.do_q115(answer, api)

            elif answer.question.pk == 117:
                api.do_q117(answer, api)

            elif answer.question.pk == 118:
                api.do_q118(answer, api)

            elif answer.question.pk == 120:
                api.do_q120(answer, api)

            elif answer.question.pk == 123:
                api.do_q123(answer, api)

            elif answer.question.pk == 125:
                api.do_q125(answer, api)

            elif answer.question.pk == 127:
                api.do_q127(answer, api)

            elif answer.question.pk == 129:
                api.do_q129(answer, api)

            elif answer.question.pk == 131:
                api.do_q131(answer, api)

            elif answer.question.pk == 133:
                api.do_q133(answer, api)

            elif answer.question.pk == 135:
                api.do_q135(answer, api)

            elif answer.question.pk == 136:
                api.do_q136(answer, api)

            elif answer.question.pk == 137:
                api.do_q137(answer, api)

            elif answer.question.pk == 138:
                api.do_q138(answer, api)

            elif answer.question.pk == 163:
                api.do_q163(answer, api)

            elif answer.question.pk == 167:
                api.do_q167(answer, api)


    def do_date(self, api):
        today = timezone.now()
        api.add_text("date", "{:%Y-%m-%d}".format(today))

    def do_owner_names(self, workspace, api):
        names = ""
        for me in workspace.mes.all():
            if names == "":
                names += str(me)
            else:
                names += ", " + str(me)
        api.add_text("owner_names", names)
