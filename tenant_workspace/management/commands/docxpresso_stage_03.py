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

    def begin_processing(self, workspace_id, api):
        workspace = self.get_workspace(workspace_id)
        answers = self.get_answers(workspace_id)
        self.process(workspace, answers, api)

    def process(self, workspace, answers, api):
        # DEBUGGING PURPOSES
        # for answer in answers.all():
        #     print(answer.question.id, answer)

        api.new(
            name="workspace_" + str(workspace.id) + "_stage_03",
            format="odt",
            template="templates/stage3.odt"
        )

        # Take our content and populate docxpresso with it.
        self.set_answers(answers, api)

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

    def set_answers(self, answers, api):
        for answer in answers.all():
            if answer.question.pk == 21: # workspace_name
                self.do_q21(answer, api)

            if answer.question.pk == 25: # naics_industry_friendly_name
                self.do_q25(answer, api)

            elif answer.question.pk == 27: # business_idea
                self.do_q27(answer, api)

            elif answer.question.pk == 28: # research_sources
                self.do_q28(answer, api)

            elif answer.question.pk == 32: # product_categories
                self.do_q32(answer, api)

            elif answer.question.pk == 33: # customer_type
                self.do_q33(answer, api)

            elif answer.question.pk == 34: # business_oppportunity
                self.do_q34(answer, api)

            elif answer.question.pk == 35: # not_being_done_because
                self.do_q35(answer, api)

            elif answer.question.pk == 36: # business_solution
                self.do_q36(answer, api)

            elif answer.question.pk == 37: # pestel_trends
                self.do_q37(answer, api)

            elif answer.question.pk == 38: # specific_sources
                self.do_q38(answer, api)

            elif answer.question.pk == 39: # geographic_market
                self.do_q39(answer, api)

            elif answer.question.pk == 40: # geographic_market | customer_buying_decision
                self.do_q40(answer, api)

            elif answer.question.pk == 50: # customer_buying_decision
                self.do_q50(answer, api)

            elif answer.question.pk == 74: # how_to_convince
                self.do_q74(answer, api)

            elif answer.question.pk == 151: # product_distribution
                self.do_q151(answer, api)

            elif answer.question.pk == 49: # target_market_characteristics
                self.do_q49(answer, api)

            elif answer.question.pk == 52: # customers_will_purchase
                self.do_q52(answer, api)

    def do_q21(self, answer, api):
        api.add_text("workspace_name", answer.content['var_1'])

    def do_q25(self, answer, api):
        api.add_text("naics_industry_friendly_name", answer.content['var_6'])

    def do_q27(self, answer, api):
        api.add_text("business_idea", answer.content['var_1'])

    def do_q28(self, answer, api):
        array = [
            answer.content['var_1'],
            answer.content['var_2'],
            answer.content['var_3']
        ];
        api.add_text_paragraphs("research_sources", array)

    def do_q32(self, answer, api):
        array = [
            answer.content['var_1'],
            answer.content['var_2'],
            answer.content['var_3']
        ];
        api.add_text_paragraphs("product_categories", array)

    def do_q33(self, answer, api):
        api.add_text(
            "customer_type",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q34(self, answer, api):
        api.add_text(
            "business_oppportunity",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q35(self, answer, api):
        api.add_text(
            "not_being_done_because",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q36(self, answer, api):
        api.add_text(
            "business_solution",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q37(self, answer, api):
        array = []
        for ans in answer.content:
            array.append(ans['var_3'])
        api.add_unordered_list("pestel_trends", array)

    def do_q38(self, answer, api):
        array = []
        for ans in answer.content:
            array.append(ans['var_2'])
        api.add_unordered_list("specific_sources", array)

    def do_q39(self, answer, api):
        api.add_text(
            "geographic_market",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q40(self, answer, api): # customer_buying_decision | geographic_market
        api.add_text(
            "geographic_market_details",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q50(self, answer, api): # customer_buying_decision | geographic_market
        api.add_text(
            "customer_buying_decision",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q74(self, answer, api):
        array = []
        for ans in answer.content['var_1']:
            array.append(ans['value'])
        api.add_text_paragraphs("how_to_convince", array)

    def do_q151(self, answer, api):
        api.add_text(
            "product_distribution",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q49(self, answer, api):
        # Debugging purposes only.
        # print(answer.question.id)
        # print(answer)
        # print(answer.content)
        # print("\n")

        array = []
        for ans in answer.content:
            array.append(ans['var_2'] + " - " + ans['var_3'] + " - " + ans['var_4'])
        api.add_text_paragraphs("target_market_characteristics", array)

    def do_q52(self, answer, api):
        api.add_text(
            "customers_will_purchase",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )
