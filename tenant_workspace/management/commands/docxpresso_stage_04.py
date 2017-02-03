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

        # Take our stage 2 content and populate docxpresso with it.
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
        api.add_text("system_date", str(workspace.created))

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

    def do_q21(self, answer, api):
        api.add_text("business_name", answer.content['var_1'])

    def do_q41(self, answer, api):
        api.add_text(
            "industry_size",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q42(self, answer, api):
        text = answer.content['var_1']
        if answer.content['var_2_other']:
            text += _(" by ") + answer.content['var_2_other']
        else:
            text += _(" by ") + answer.content['var_2']
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
        names_array = []
        proximities_array = []
        market_shares_array = []
        price_comparisons_array = []
        service_levels_array = []
        main_strengths_array = []
        competitive_strategy_array = []

        for ans in answer.content:
            names_array.append(ans['var_2'])
            proximities_array.append(ans['var_3'])
            market_shares_array.append(ans['var_4'])
            price_comparisons_array.append(ans['var_5'])
            main_strengths_array.append(ans['var_7'])
            service_levels_array.append(ans['var_6'])
            competitive_strategy_array.append(ans['var_8'])

        # --- Debugging purposes. ---
        # print("Name", names_array)
        # print("Prox", proximities_array)
        # print("Market", market_shares_array)
        # print("Price", price_comparisons_array)
        # print("Strength", main_strengths_array)
        # print("Customer", service_levels_array)
        # print("Competitive", competitive_strategy_array)
        # print("\n")

        # Generate our custom item.
        names_dict = {
            "var": 'dc_names',
            'value': names_array
        }
        proximities_dict = {
            "var": 'dc_proximities',
            'value': proximities_array
        }
        market_shares_dict = {
            "var": 'dc_market_shares',
            'value': market_shares_array
        }
        price_comparisons_dict = {
            "var": 'dc_price_comparisons',
            'value': price_comparisons_array
        }
        main_strengths_dict = {
            "var": 'dc_main_strengths',
            'value': main_strengths_array
        }
        service_levels_dict = {
            "var": 'dc_service_levels',
            'value': service_levels_array
        }
        competitive_strategy_dict = {
            "var": 'dc_competitive_strategy',
            'value': competitive_strategy_array
        }

        # --- Debugging purposes only. ---
        # print("Name", names_dict)
        # print("Proximities", proximities_dict)
        # print("market_shares", market_shares_dict)
        # print("price_comparisons", price_comparisons_dict)
        # print("main_strengths", main_strengths_dict)
        # print("service_levels", service_levels_dict)
        # print("competitive_strategy", competitive_strategy_dict)

        # Generate the custom API query.
        custom = {
            "vars": [
                names_dict,
                proximities_dict,
                market_shares_dict,
                price_comparisons_dict,
                main_strengths_dict,
                service_levels_dict,
                competitive_strategy_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # --- Debugging purposes only. ---
        # print(custom)

        # Attach all out tables.
        api.add_custom(custom)

    def do_q48(self, answer, api):
        names_array = []
        proximities_array = []
        market_shares_array = []
        price_comparisons_array = []
        service_levels_array = []
        main_strengths_array = []
        competitive_strategy_array = []

        for ans in answer.content:
            names_array.append(ans['var_2'])
            proximities_array.append(ans['var_3'])
            market_shares_array.append(ans['var_4'])
            price_comparisons_array.append(ans['var_5'])
            main_strengths_array.append(ans['var_7'])
            service_levels_array.append(ans['var_6'])
            competitive_strategy_array.append(ans['var_8'])

        # --- Debugging purposes. ---
        # print("Name", names_array)
        # print("Prox", proximities_array)
        # print("Market", market_shares_array)
        # print("Price", price_comparisons_array)
        # print("Strength", main_strengths_array)
        # print("Customer", service_levels_array)
        # print("Competitive", competitive_strategy_array)
        # print("\n")

        # Generate our custom item.
        names_dict = {
            "var": 'idc_names',
            'value': names_array
        }
        proximities_dict = {
            "var": 'idc_proximities',
            'value': proximities_array
        }
        market_shares_dict = {
            "var": 'idc_market_shares',
            'value': market_shares_array
        }
        price_comparisons_dict = {
            "var": 'idc_price_comparisons',
            'value': price_comparisons_array
        }
        main_strengths_dict = {
            "var": 'idc_main_strengths',
            'value': main_strengths_array
        }
        service_levels_dict = {
            "var": 'idc_service_levels',
            'value': service_levels_array
        }
        competitive_strategy_dict = {
            "var": 'idc_competitive_strategy',
            'value': competitive_strategy_array
        }

        # --- Debugging purposes only. ---
        # print("Name", names_dict)
        # print("Proximities", proximities_dict)
        # print("market_shares", market_shares_dict)
        # print("price_comparisons", price_comparisons_dict)
        # print("main_strengths", main_strengths_dict)
        # print("service_levels", service_levels_dict)
        # print("competitive_strategy", competitive_strategy_dict)

        # Generate the custom API query.
        custom = {
            "vars": [
                names_dict,
                proximities_dict,
                market_shares_dict,
                price_comparisons_dict,
                main_strengths_dict,
                service_levels_dict,
                # competitive_strategy_dict  # To not include this field.
            ],
            "options": {
                "element": "table"
            }
        }

        # --- Debugging purposes only. ---
        # print(custom)

        # Attach all out tables.
        api.add_custom(custom)

    def do_q150(self, answer, api):
        text = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        api.add_text("industry_competition_amount", text)

    def do_q152(self, answer, api):
        text = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        api.add_text("avg_customer_spending", text)
