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
            self.style.SUCCESS(_('Finished processing stage 4 for workspace_id #%s.') % str(workspace_id))
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
                document_type__stage_num=4
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
                document__document_type__stage_num=4
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
            name="workspace_" + str(workspace.id) + "_stage_04",
            format="odt",
            template="templates/stage4.odt"
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
        self.do_system_date(workspace, api)

        for answer in answers.all():
            if answer.question.pk == 21:
                self.do_q21(answer, api)

            if answer.question.pk == 41:
                self.do_q41(answer, api)

            elif answer.question.pk == 42:
                self.do_q42(answer, api)

            elif answer.question.pk == 43:
                self.do_q43(answer, api)

            elif answer.question.pk == 44:
                self.do_q44(answer, api)

            elif answer.question.pk == 45:
                self.do_q45(answer, api)

            elif answer.question.pk == 46:
                self.do_q46(answer, api)

            elif answer.question.pk == 47:
                self.do_q47(answer, api)

            elif answer.question.pk == 48:
                self.do_q48(answer, api)

            elif answer.question.pk == 150:
                self.do_q150(answer, api)

            elif answer.question.pk == 152:
                self.do_q152(answer, api)

            elif answer.question.pk == 169:
                self.do_q169(answer, api)

    def do_system_date(self, workspace, api):
        api.add_text("system_date", "{:%Y-%m-%d}".format(workspace.created))

    def do_q21(self, answer, api):
        api.add_text("business_name", answer.content['var_1'])

    def do_q41(self, answer, api):
        api.add_text(
            "industry_size",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q42(self, answer, api):
        # Item 1
        text = answer.content['var_1']
        api.add_text("industry_change_type",text)

        # Item 2
        text = None
        if answer.content['var_2_other']:
            text = answer.content['var_2_other']
        else:
            text = answer.content['var_2']
        api.add_text("industry_change_rate",text)

    def do_q43(self, answer, api):
        text = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        api.add_text("total_potential_customer_base", text)

    def do_q44(self, answer, api):
        text = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        api.add_text("industry_competition_level", text)

    def do_q45(self, answer, api):
        text = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        api.add_text("industry_service_level", text)

    def do_q46(self, answer, api):
        text = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        api.add_text("industry_price_variation", text)

    def do_q47(self, answer, api):
        self.do_type43(
            answer,
            api,
            'dc_names',
            'dc_proximities',
            'dc_market_shares',
            'dc_price_comparisons',
            'dc_main_strengths',
            'dc_service_levels',
            'dc_competitive_strategy'
        )

    def do_q48(self, answer, api):
        self.do_type43(
            answer,
            api,
            'idc_names',
            'idc_proximities',
            'idc_market_shares',
            'idc_price_comparisons',
            'idc_main_strengths',
            'idc_service_levels',
            'idc_competitive_strategy'
        )

    def do_q150(self, answer, api):
        text = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        api.add_text("industry_competition_amount", text)

    def do_q152(self, answer, api):
        text = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        api.add_text("avg_customer_spending", text)

    def do_q169(self, answer, api):
        text = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        api.add_text("supplier_amount", text)

    def do_type43(self, answer, api, key1, key2, key3, key4, key5, key6, key7):  # 7 Col Table
        col1_array = []
        col2_array = []
        col3_array = []
        col4_array = []
        col5_array = []
        col6_array = []
        col7_array = []

        # Populate rows.
        for ans in answer.content:
            col1_array.append(ans['var_2'])
            col2_array.append(ans['var_3'])
            col3_array.append(ans['var_4'])
            col4_array.append(ans['var_5'])
            col5_array.append(ans['var_6'])
            col6_array.append(ans['var_7'])
            col7_array.append(ans['var_8'])

        # Generate our custom item.
        c1_dict = {"var": key1, 'value': col1_array}
        c2_dict = {"var": key2, 'value': col2_array}
        c3_dict = {"var": key3, 'value': col3_array}
        c4_dict = {"var": key4, 'value': col4_array}
        c5_dict = {"var": key5, 'value': col5_array}
        c6_dict = {"var": key6, 'value': col6_array}
        c7_dict = {"var": key7, 'value': col7_array}

        # print(c1_dict)
        # print(c2_dict)
        # print(c3_dict)
        # print(c4_dict)
        # print(c5_dict)
        # print(c6_dict)
        # print(c7_dict)
        # print("\n\n")

        # Generate the custom API query.
        custom = {
            "vars": [
                c1_dict,
                c2_dict,
                c3_dict,
                c4_dict,
                c5_dict,
                c6_dict,
                c7_dict,
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)
