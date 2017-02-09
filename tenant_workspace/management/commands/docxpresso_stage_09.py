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
from foundation_tenant.bizmula_utils import BizmulaAPI
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
            template="templates/stage9.odt"
        )

        # Take our content and populate docxpresso with it.
        self.set_answers(workspace, answers, api)

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

    def set_answers(self, workspace, answers, api):
        # Assign date.
        self.do_date(api)

        # Iterate through all the answers and transcode the business plan.
        for answer in answers.all():
            if answer.question.pk == 1:
                api.do_q1(answer, api)

            elif answer.question.pk == 2:
                api.do_q2(answer, api)

            elif answer.question.pk == 3:
                api.do_q3(answer, api)

            elif answer.question.pk == 4:
                api.do_q4(answer, api)

            elif answer.question.pk == 5:
                api.do_q5(answer, api)

            elif answer.question.pk == 6:
                api.do_q6(answer, api)

            elif answer.question.pk == 7:
                api.do_q7(answer, api)

            elif answer.question.pk == 8:
                api.do_q8(answer, api)

            elif answer.question.pk == 9:
                api.do_q9(answer, api)

            elif answer.question.pk == 10:
                api.do_q10(answer, api)

            elif answer.question.pk == 21:
                api.do_q21(answer, api)

            elif answer.question.pk == 25:
                api.do_q25(answer, api)

            elif answer.question.pk == 26:
                api.do_q26(answer, api)

            elif answer.question.pk == 27:
                api.do_q27(answer, api)

            elif answer.question.pk == 28:
                api.do_q28(answer, api)

            elif answer.question.pk == 29:
                api.do_q29(answer, api)

            elif answer.question.pk == 30:
                api.do_q30(answer, api)

            # elif answer.question.pk == 32:
            #     api.do_q32(answer, api)

            elif answer.question.pk == 33:
                api.do_q33(answer, api)

            elif answer.question.pk == 34:
                api.do_q34(answer, api)

            elif answer.question.pk == 35:
                api.do_q35(answer, api)

            elif answer.question.pk == 36:
                api.do_q36(answer, api)

            elif answer.question.pk == 37:
                api.do_q37(answer, api)

            elif answer.question.pk == 38:
                api.do_q38(answer, api)

            elif answer.question.pk == 39:
                api.do_q39(answer, api)

            elif answer.question.pk == 40:
                api.do_q40(answer, api)

            elif answer.question.pk == 41:
                api.do_q41(answer, api)

            elif answer.question.pk == 42:
                api.do_q42(answer, api)

            elif answer.question.pk == 43:
                api.do_q43(answer, api)

            elif answer.question.pk == 44:
                api.do_q44(answer, api)

            elif answer.question.pk == 45:
                api.do_q45(answer, api)

            elif answer.question.pk == 46:
                api.do_q46(answer, api)

            elif answer.question.pk == 47:
                api.do_q47(answer, api)

            elif answer.question.pk == 48:
                api.do_q48(answer, api)

            elif answer.question.pk == 49:
                api.do_q49(answer, api)

            elif answer.question.pk == 51:
                api.do_q51(answer, api)

            elif answer.question.pk == 52:
                api.do_q52(answer, api)

            elif answer.question.pk == 53:
                api.do_q53(answer, api)

            elif answer.question.pk == 54:
                api.do_q54(answer, api)

            elif answer.question.pk == 55:
                api.do_q55(answer, api)

            elif answer.question.pk == 56:
                # actual_contact_number
                api.do_q56(answer, api)

            elif answer.question.pk == 58:
                # actual_supported_number
                # validation_outcome_met
                api.do_q58(answer, api, answers)

            elif answer.question.pk == 59:
                # validation_lessons_learned
                api.do_q59(answer, api)

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

            elif answer.question.pk == 73:
                api.do_q73(answer, api)

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

            elif answer.question.pk == 81:
                api.do_q81(answer, api)

            elif answer.question.pk == 82:
                api.do_q82(answer, api)

            elif answer.question.pk == 83:
                api.do_q83(answer, api)

            elif answer.question.pk == 87:
                api.do_q87(answer, api)

            elif answer.question.pk == 88:
                api.do_q88(answer, api)

            elif answer.question.pk == 91:
                api.do_q91(answer, api)

            elif answer.question.pk == 92:
                api.do_q92(answer, api)

            elif answer.question.pk == 93:
                api.do_q93(answer, api)

            elif answer.question.pk == 97:
                api.do_q97(answer, api)

            elif answer.question.pk == 98:
                api.do_q98(answer, api)

            elif answer.question.pk == 99:
                api.do_q99(answer, api)

            elif answer.question.pk == 100:
                api.do_q100(answer, api)

            elif answer.question.pk == 101:
                api.do_q101(answer, api)

            elif answer.question.pk == 102:
                api.do_q102(answer, api)

            elif answer.question.pk == 103:
                api.do_q103(answer, api)

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

            elif answer.question.pk == 150:
                api.do_q150(answer, api)

            elif answer.question.pk == 151:
                api.do_q151(answer, api)

            elif answer.question.pk == 152:
                api.do_q152(answer, api)

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
