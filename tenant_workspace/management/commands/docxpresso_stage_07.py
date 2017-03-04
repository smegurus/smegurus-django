# -*- coding: utf-8 -*-
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
            self.style.SUCCESS(_('Finished processing stage 7 for workspace_id #%s.') % str(workspace_id))
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
                document_type__stage_num=7
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
            name="workspace_" + str(workspace.id) + "_stage_07",
            format="odt",
            template="templates/stage7.odt"
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
            if answer.question.pk == 25:
                api.do_q25(answer, api)

            elif answer.question.pk == 27:
                api.do_q27(answer, api)

            elif answer.question.pk == 32:
                api.do_q32(answer, api)

            elif answer.question.pk == 44:
                api.do_q44(answer, api)

            elif answer.question.pk == 47:
                api.do_q47(answer, api)

            elif answer.question.pk == 48:
                api.do_q48(answer, api)

            elif answer.question.pk == 49:
                api.do_q49(answer, api)

            elif answer.question.pk == 61:
                api.do_q61(answer, api)

            elif answer.question.pk == 62:
                api.do_q62(answer, api)

            elif answer.question.pk == 63:
                api.do_q63(answer, api)

            elif answer.question.pk == 64:
                api.do_q64(answer, api)

            elif answer.question.pk == 65:
                api.do_q65(answer, api)

            elif answer.question.pk == 66:
                api.do_q66(answer, api)

            elif answer.question.pk == 67:
                api.do_q67(answer, api)

            elif answer.question.pk == 68:
                api.do_q68(answer, api)

            elif answer.question.pk == 69:
                api.do_q69(answer, api)

            elif answer.question.pk == 70:
                api.do_q70(answer, api)

            elif answer.question.pk == 71:
                api.do_q71(answer, api)

            elif answer.question.pk == 72:
                api.do_q72(answer, api)

            elif answer.question.pk == 74:
                api.do_q74(answer, api)

            elif answer.question.pk == 75:
                api.do_q75(answer, api)

            elif answer.question.pk == 76:
                api.do_q76(answer, api)

            elif answer.question.pk == 77:
                api.do_q77(answer, api)

            elif answer.question.pk == 78:
                api.do_q78(answer, api)

            elif answer.question.pk == 79:
                api.do_q79(answer, api)

            elif answer.question.pk == 80:
                api.do_q80(answer, api)

            elif answer.question.pk == 104:
                api.do_q104(answer, api)

            elif answer.question.pk == 142:
                api.do_q142(answer, api)

            elif answer.question.pk == 142:
                api.do_q142(answer, api)

            elif answer.question.pk == 143:
                api.do_q143(answer, api)

            elif answer.question.pk == 147:
                api.do_q147(answer, api)

            elif answer.question.pk == 148:
                api.do_q148(answer, api)

            elif answer.question.pk == 149:
                api.do_q149(answer, api)

            elif answer.question.pk == 151:
                api.do_q151(answer, api)

            elif answer.question.pk == 153:
                api.do_q153(answer, api)

            elif answer.question.pk == 154:
                api.do_q154(answer, api)

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
