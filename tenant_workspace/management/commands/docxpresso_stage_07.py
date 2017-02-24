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
        # DEBUGGING PURPOSES
        # for answer in answers.all():
        #     print(answer.question.id, answer)

        api.new(
            name="workspace_" + str(workspace.id) + "_stage_07",
            format="odt",
            template="templates/stage7.odt"
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
        self.do_date(api)

        for answer in answers.all():
            if answer.question.pk == 25:
                self.do_q25(answer, api)

            elif answer.question.pk == 27:
                self.do_q27(answer, api)

            elif answer.question.pk == 32:
                self.do_q32(answer, api)

            elif answer.question.pk == 44:
                self.do_q44(answer, api)

            elif answer.question.pk == 47:
                self.do_q47(answer, api)

            elif answer.question.pk == 48:
                self.do_q48(answer, api)

            elif answer.question.pk == 49:
                self.do_q49(answer, api)

            elif answer.question.pk == 61:
                self.do_q61(answer, api)

            elif answer.question.pk == 62:
                self.do_q62(answer, api)

            elif answer.question.pk == 63:
                self.do_q63(answer, api)

            elif answer.question.pk == 64:
                self.do_q64(answer, api)

            elif answer.question.pk == 65:
                self.do_q65(answer, api)

            elif answer.question.pk == 66:
                self.do_q66(answer, api)

            elif answer.question.pk == 67:
                self.do_q67(answer, api)

            elif answer.question.pk == 68:
                self.do_q68(answer, api)

            elif answer.question.pk == 69:
                self.do_q69(answer, api)

            elif answer.question.pk == 70:
                self.do_q70(answer, api)

            elif answer.question.pk == 71:
                self.do_q71(answer, api)

            elif answer.question.pk == 72:
                self.do_q72(answer, api)

            elif answer.question.pk == 74:
                self.do_q74(answer, api)

            elif answer.question.pk == 75:
                self.do_q75(answer, api)

            elif answer.question.pk == 76:
                self.do_q76(answer, api)

            elif answer.question.pk == 77:
                self.do_q77(answer, api)

            elif answer.question.pk == 78:
                self.do_q78(answer, api)

            elif answer.question.pk == 79:
                self.do_q79(answer, api)

            elif answer.question.pk == 80:
                self.do_q80(answer, api)

            elif answer.question.pk == 104:
                self.do_q104(answer, api)

            elif answer.question.pk == 142:
                self.do_q142(answer, api)

            elif answer.question.pk == 142:
                self.do_q142(answer, api)

            elif answer.question.pk == 143:
                self.do_q143(answer, api)

            elif answer.question.pk == 147:
                self.do_q147(answer, api)

            elif answer.question.pk == 148:
                self.do_q148(answer, api)

            elif answer.question.pk == 149:
                self.do_q149(answer, api)

            elif answer.question.pk == 151:
                self.do_q151(answer, api)

            elif answer.question.pk == 153:
                self.do_q153(answer, api)

            elif answer.question.pk == 154:
                self.do_q154(answer, api)

    def do_date(self, api):
        today = timezone.now()
        api.add_text("date", "{:%Y-%m-%d}".format(today))

    def do_q25(self, answer, api):
        naics_id = answer.content['var_5'] # Depth 5 NAICS ID
        depth_five_naics = NAICSOption.objects.get(id=naics_id) # Get the name
        api.add_text("naics_industry_name", depth_five_naics.name)
        api.add_text("naics_industry_friendly_name", answer.content['var_6'])

    def do_q27(self, answer, api):
        api.add_text("business_idea", answer.content['var_1'])

    def do_q32(self, answer, api):
        array = [
            answer.content['var_1'],
            answer.content['var_2'],
            answer.content['var_3']
        ];
        api.add_text_paragraphs("product_categories", array)

    def do_q44(self, answer, api):
        text = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        api.add_text("industry_competition_levels", text)

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
            "var": 'dc_how_compete',
            'value': competitive_strategy_array
        }

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
            "var": 'idc_how_compete',
            'value': competitive_strategy_array
        }

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

        # Attach all out tables.
        api.add_custom(custom)

    def do_q49(self, answer, api):
        target_market_types_array = []
        target_market_first_traits_array = []
        target_market_second_traits_array = []
        for ans in answer.content:
            target_market_types_array.append(ans['var_2'])
            target_market_first_traits_array.append(ans['var_3'])
            target_market_second_traits_array.append(ans['var_4'])

        api.add_text_paragraphs("target_market_types", target_market_types_array)
        api.add_text_paragraphs("target_market_first_traits", target_market_first_traits_array)
        api.add_text_paragraphs("target_market_second_traits", target_market_second_traits_array)

    def do_q61(self, answer, api):
        api.add_text('business_formal_name', answer.content['var_1'])
        api.add_text('business_friendly_name', answer.content['var_3'])

    def do_q62(self, answer, api):
        business_weaknesses_array = []
        business_weakness_resolutions_array = []

        # Populate rows.
        for ans in answer.content:
            business_weaknesses_array.append(ans['var_2'])
            business_weakness_resolutions_array.append(ans['var_3'])

        # Generate our custom item.
        business_weaknesses_dict = {
            "var": 'business_weaknesses',
            'value': business_weaknesses_array
        }
        business_weakness_resolutions_dict = {
            "var": 'business_weakness_resolutions',
            'value': business_weakness_resolutions_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                business_weaknesses_dict,
                business_weakness_resolutions_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q63(self, answer, api): #BUG: NULL IS BEING RETURNED, MUST INVESTIGATE.
        api.add_text('business_mission', answer.content['var_2'])

    def do_q64(self, answer, api):
        api.add_text('business_vision', answer.content['var_2'])

    def do_q65(self, answer, api):
        api.add_text(
            "product_customer_need",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q66(self, answer, api):
        api.add_text(
            "business_how_different",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q67(self, answer, api):
        api.add_text(
            "market_position",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )
        api.add_text(
            "market_position_details",
            answer.content['var_2_other'] if answer.content['var_2_other'] else answer.content['var_2']
        )

    def do_q68(self, answer, api):
        api.add_text(
            "business_great_at",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q69(self, answer, api):
        api.add_text(
            "pricing_strategy",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q70(self, answer, api):
        api.add_text(
            "how_customer_buys",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q71(self, answer, api):
        api.add_text(
            "distribution_challenge",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )
        api.add_text(
            "distribution_challenge_resolution",
            answer.content['var_2_other'] if answer.content['var_2_other'] else answer.content['var_2']
        )

    def do_q72(self, answer, api):
        array = []

        if answer.content['var_1_other']:
            array.append(answer.content['var_1_other'])
        else:
            array.append(answer.content['var_1'])

        if answer.content['var_2_other']:
            array.append(answer.content['var_2_other'])
        else:
            array.append(answer.content['var_2'])

        if answer.content['var_3_other']:
            array.append(answer.content['var_3_other'])
        else:
            array.append(answer.content['var_3'])

        api.add_text_paragraphs('key_success_factors', array)

    def do_q74(self, answer, api):
        array = []
        for ans in answer.content['var_1']:
            array.append(ans['value'])
        api.add_text_paragraphs("how_to_convince", array)

    def do_q75(self, answer, api):
        customer_objections_array = []
        customer_objection_responses_array = []

        # Populate rows.
        for ans in answer.content:
            customer_objections_array.append(ans['var_2'])
            customer_objection_responses_array.append(ans['var_3'])

        # Generate our custom item.
        customer_objections_dict = {
            "var": 'customer_objections',
            'value': customer_objections_array
        }
        customer_objection_responses_dict = {
            "var": 'customer_objection_responses',
            'value': customer_objection_responses_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                customer_objections_dict,
                customer_objection_responses_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q76(self, answer, api):
        api.add_text(
            "customer_buying_time",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q77(self, answer, api):
        incentive_types_array = []
        incentive_impacts_array = []
        incentive_durations_array = []
        incentive_cost_types_array = []
        incentive_y1_costs_array = []
        incentive_y2_costs_array = []
        incentive_y3_costs_array = []

        # Populate rows.
        for ans in answer.content:
            incentive_types_array.append(ans['var_2'])
            incentive_impacts_array.append(ans['var_3'])
            incentive_durations_array.append(ans['var_4'])
            incentive_cost_types_array.append(ans['var_5'])
            incentive_y1_costs_array.append(ans['var_6'])
            incentive_y2_costs_array.append(ans['var_7'])
            incentive_y3_costs_array.append(ans['var_8'])

        # Generate our custom item.
        incentive_types_dict = {
            "var": 'incentive_types',
            'value': incentive_types_array
        }
        incentive_impacts_dict = {
            "var": 'incentive_impacts',
            'value': incentive_impacts_array
        }
        incentive_durations_dict = {
            "var": 'incentive_durations',
            'value': incentive_durations_array
        }
        incentive_cost_types_dict = {
            "var": 'incentive_cost_types',
            'value': incentive_cost_types_array
        }
        incentive_y1_costs_dict = {
            "var": 'incentive_y1_costs',
            'value': incentive_y1_costs_array
        }
        incentive_y2_costs_dict = {
            "var": 'incentive_y2_costs',
            'value': incentive_y2_costs_array
        }
        incentive_y3_costs_dict = {
            "var": 'incentive_y3_costs',
            'value': incentive_y3_costs_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                incentive_types_dict,
                incentive_impacts_dict,
                incentive_durations_dict,
                # incentive_cost_types_dict,
                incentive_y1_costs_dict,
                # incentive_y2_costs_dict,
                # incentive_y3_costs_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q78(self, answer, api):
        physical_marketing_types_array = []
        physical_marketing_impacts_array = []
        physical_marketing_uses_array = []
        physical_marketing_cost_types_array = []
        physical_marketing_y1_costs_array = []
        physical_marketing_y2_costs_array = []
        physical_marketing_y3_costs_array = []

        # Populate rows.
        for ans in answer.content:
            physical_marketing_types_array.append(ans['var_2'])
            physical_marketing_impacts_array.append(ans['var_3'])
            physical_marketing_uses_array.append(ans['var_4'])
            physical_marketing_cost_types_array.append(ans['var_5'])
            physical_marketing_y1_costs_array.append(ans['var_6'])
            physical_marketing_y2_costs_array.append(ans['var_7'])
            physical_marketing_y3_costs_array.append(ans['var_8'])

        # Generate our custom item.
        physical_marketing_types_dict = {
            "var": 'physical_marketing_types',
            'value': physical_marketing_types_array
        }
        physical_marketing_impacts_dict = {
            "var": 'physical_marketing_impacts',
            'value': physical_marketing_impacts_array
        }
        physical_marketing_uses_dict = {
            "var": 'physical_marketing_uses',
            'value': physical_marketing_uses_array
        }
        physical_marketing_cost_types_dict = {
            "var": 'physical_marketing_cost_types',
            'value': physical_marketing_cost_types_array
        }
        physical_marketing_y1_costs_dict = {
            "var": 'physical_marketing_y1_costs',
            'value': physical_marketing_y1_costs_array
        }
        physical_marketing_y2_costs_dict = {
            "var": 'physical_marketing_y2_costs',
            'value': physical_marketing_y2_costs_array
        }
        physical_marketing_y3_costs_dict = {
            "var": 'physical_marketing_y3_costs',
            'value': physical_marketing_y3_costs_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                physical_marketing_types_dict,
                physical_marketing_impacts_dict,
                physical_marketing_uses_dict,
                # physical_marketing_cost_types_dict,
                physical_marketing_y1_costs_dict,
                # physical_marketing_y2_costs_dict,
                # physical_marketing_y3_costs_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q79(self, answer, api):
        media_campaign_types_array = []
        media_campaign_impacts_array = []
        media_campaign_durations_array = []
        media_campaign_cost_types_array = []
        media_campaign_y1_costs_array = []
        media_campaign_y2_costs_array = []
        media_campaign_y3_costs_array = []

        # Populate rows.
        for ans in answer.content:
            media_campaign_types_array.append(ans['var_2'])
            media_campaign_impacts_array.append(ans['var_3'])
            media_campaign_durations_array.append(ans['var_4'])
            media_campaign_cost_types_array.append(ans['var_5'])
            media_campaign_y1_costs_array.append(ans['var_6'])
            media_campaign_y2_costs_array.append(ans['var_7'])
            media_campaign_y3_costs_array.append(ans['var_8'])

        # Generate our custom item.
        media_campaign_types_dict = {
            "var": 'media_campaign_types',
            'value': media_campaign_types_array
        }
        media_campaign_impacts_dict = {
            "var": 'media_campaign_impacts',
            'value': media_campaign_impacts_array
        }
        media_campaign_durations_dict = {
            "var": 'media_campaign_durations',
            'value': media_campaign_durations_array
        }
        media_campaign_cost_types_dict = {
            "var": 'media_campaign_cost_types',
            'value': media_campaign_cost_types_array
        }
        media_campaign_y1_costs_dict = {
            "var": 'media_campaign_y1_costs',
            'value': media_campaign_y1_costs_array
        }
        media_campaign_y2_costs_dict = {
            "var": 'media_campaign_y2_costs',
            'value': media_campaign_y2_costs_array
        }
        media_campaign_y3_costs_dict = {
            "var": 'media_campaign_y3_costs',
            'value': media_campaign_y3_costs_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                media_campaign_types_dict,
                media_campaign_impacts_dict,
                media_campaign_durations_dict,
                # media_campaign_cost_types_dict,
                media_campaign_y1_costs_dict,
                # media_campaign_y2_costs_dict,
                # media_campaign_y3_costs_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q80(self, answer, api):
        marketing_partnership_types_array = []
        marketing_partnership_impacts_array = []
        marketing_partnership_durations_array = []
        marketing_partnership_cost_types_array = []
        marketing_partnership_y1_costs_array = []
        marketing_partnership_y2_costs_array = []
        marketing_partnership_y3_costs_array = []

        # Populate rows.
        for ans in answer.content:
            marketing_partnership_types_array.append(ans['var_2'])
            marketing_partnership_impacts_array.append(ans['var_3'])
            marketing_partnership_durations_array.append(ans['var_4'])
            marketing_partnership_cost_types_array.append(ans['var_5'])
            marketing_partnership_y1_costs_array.append(ans['var_6'])
            marketing_partnership_y2_costs_array.append(ans['var_7'])
            marketing_partnership_y3_costs_array.append(ans['var_8'])

        # Generate our custom item.
        marketing_partnership_types_dict = {
            "var": 'marketing_partnership_types',
            'value': marketing_partnership_types_array
        }
        marketing_partnership_impacts_dict = {
            "var": 'marketing_partnership_impacts',
            'value': marketing_partnership_impacts_array
        }
        marketing_partnership_durations_dict = {
            "var": 'marketing_partnership_durations',
            'value': marketing_partnership_durations_array
        }
        marketing_partnership_cost_types_dict = {
            "var": 'marketing_partnership_cost_types',
            'value': marketing_partnership_cost_types_array
        }
        marketing_partnership_y1_costs_dict = {
            "var": 'marketing_partnership_y1_costs',
            'value': marketing_partnership_y1_costs_array
        }
        marketing_partnership_y2_costs_dict = {
            "var": 'marketing_partnership_y2_costs',
            'value': marketing_partnership_y2_costs_array
        }
        marketing_partnership_y3_costs_dict = {
            "var": 'marketing_partnership_y3_costs',
            'value': marketing_partnership_y3_costs_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                marketing_partnership_types_dict,
                marketing_partnership_impacts_dict,
                marketing_partnership_durations_dict,
                # marketing_partnership_cost_types_dict,
                marketing_partnership_y1_costs_dict,
                # marketing_partnership_y2_costs_dict,
                # marketing_partnership_y3_costs_dict
            ],
            "options": {
                "element": "table"
            }
        }


        # Attach all out tables.
        api.add_custom(custom)

    def do_q104(self, answer, api):
        # 104	7	{{marketing_costs_m1}}
        # 104	7	{{marketing_costs_m2}}
        # 104	7	{{marketing_costs_m3}}
        # 104	7	{{marketing_costs_m4}}
        # 104	7	{{marketing_costs_m5}}
        # 104	7	{{marketing_costs_m6}}
        # 104	7	{{marketing_costs_m7}}
        # 104	7	{{marketing_costs_m8}}
        # 104	7	{{marketing_costs_m9}}
        # 104	7	{{marketing_costs_m10}}
        # 104	7	{{marketing_costs_m11}}
        # 104	7	{{marketing_costs_m12}}
        # 104	7	{{marketing_costs_y1_total}}
        # 104	7	{{marketing_costs_m13}}
        # 104	7	{{marketing_costs_m14}}
        # 104	7	{{marketing_costs_m15}}
        # 104	7	{{marketing_costs_m16}}
        # 104	7	{{marketing_costs_m17}}
        # 104	7	{{marketing_costs_m18}}
        # 104	7	{{marketing_costs_m19}}
        # 104	7	{{marketing_costs_m20}}
        # 104	7	{{marketing_costs_m21}}
        # 104	7	{{marketing_costs_m22}}
        # 104	7	{{marketing_costs_m23}}
        # 104	7	{{marketing_costs_m24}}
        # 104	7	{{marketing_costs_y2_total}}
        # 104	7	{{marketing_costs_m25}}
        # 104	7	{{marketing_costs_m26}}
        # 104	7	{{marketing_costs_m27}}
        # 104	7	{{marketing_costs_m28}}
        # 104	7	{{marketing_costs_m29}}
        # 104	7	{{marketing_costs_m30}}
        # 104	7	{{marketing_costs_m31}}
        # 104	7	{{marketing_costs_m32}}
        # 104	7	{{marketing_costs_m33}}
        # 104	7	{{marketing_costs_m34}}
        # 104	7	{{marketing_costs_m35}}
        # 104	7	{{marketing_costs_m36}}
        # 104	7	{{marketing_costs_y3_total}}
        print("QID 104") #TODO: IMPLEMENT

    def do_q142(self, answer, api):
        marketing_referral_types_array = []
        marketing_referral_impacts_array = []
        marketing_referral_cost_types_array = []
        marketing_referral_y1_costs_array = []
        marketing_referral_y2_costs_array = []
        marketing_referral_y3_costs_array = []

        # Populate rows.
        for ans in answer.content:
            marketing_referral_types_array.append(ans['var_2'])
            marketing_referral_impacts_array.append(ans['var_3'])
            marketing_referral_cost_types_array.append(ans['var_4'])
            marketing_referral_y1_costs_array.append(ans['var_5'])
            marketing_referral_y2_costs_array.append(ans['var_6'])
            marketing_referral_y3_costs_array.append(ans['var_7'])

        # Generate our custom item.
        marketing_referral_types_dict = {
            "var": 'marketing_referral_types',
            'value': marketing_referral_types_array
        }
        marketing_referral_impacts_dict = {
            "var": 'marketing_referral_impacts',
            'value': marketing_referral_impacts_array
        }
        marketing_referral_cost_types_dict = {
            "var": 'marketing_referral_cost_types',
            'value': marketing_referral_cost_types_array
        }
        marketing_referral_y1_costs_dict = {
            "var": 'marketing_referral_y1_costs',
            'value': marketing_referral_y1_costs_array
        }
        marketing_referral_y2_costs_dict = {
            "var": 'marketing_referral_y2_costs',
            'value': marketing_referral_y2_costs_array
        }
        marketing_referral_y3_costs_dict = {
            "var": 'marketing_referral_y3_costs',
            'value': marketing_referral_y3_costs_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                marketing_referral_types_dict,
                marketing_referral_impacts_dict,
                # marketing_referral_cost_types_dict,
                marketing_referral_y1_costs_dict,
                # marketing_referral_y2_costs_dict,
                # marketing_referral_y3_costs_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q143(self, answer, api):
        marketing_retention_types_array = []
        marketing_retention_impacts_array = []
        marketing_retention_cost_types_array = []
        marketing_retention_y1_costs_array = []
        marketing_retention_y2_costs_array = []
        marketing_retention_y3_costs_array = []

        # Populate rows.
        for ans in answer.content:
            marketing_retention_types_array.append(ans['var_2'])
            marketing_retention_impacts_array.append(ans['var_3'])
            marketing_retention_cost_types_array.append(ans['var_4'])
            marketing_retention_y1_costs_array.append(ans['var_5'])
            marketing_retention_y2_costs_array.append(ans['var_6'])
            marketing_retention_y3_costs_array.append(ans['var_7'])

        # Generate our custom item.
        marketing_retention_types_dict = {
            "var": 'marketing_retention_types',
            'value': marketing_retention_types_array
        }
        marketing_retention_impacts_dict = {
            "var": 'marketing_retention_impacts',
            'value': marketing_retention_impacts_array
        }
        marketing_retention_cost_types_dict = {
            "var": 'marketing_retention_cost_types',
            'value': marketing_retention_cost_types_array
        }
        marketing_retention_y1_costs_dict = {
            "var": 'marketing_retention_y1_costs',
            'value': marketing_retention_y1_costs_array
        }
        marketing_retention_y2_costs_dict = {
            "var": 'marketing_retention_y2_costs',
            'value': marketing_retention_y2_costs_array
        }
        marketing_retention_y3_costs_dict = {
            "var": 'marketing_retention_y3_costs',
            'value': marketing_retention_y3_costs_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                marketing_retention_types_dict,
                marketing_retention_impacts_dict,
                # marketing_retention_cost_types_dict,
                marketing_retention_y1_costs_dict,
                # marketing_retention_y2_costs_dict,
                # marketing_retention_y3_costs_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q147(self, answer, api):
        array = []

        for ans in answer.content:
            array.append(ans['var_2'])

        api.add_text_paragraphs('business_strengths', array)

    def do_q148(self, answer, api):
        array = []

        for ans in answer.content:
            array.append(ans['var_2'])

        api.add_text_paragraphs('business_opportunities', array)

    def do_q149(self, answer, api):
        business_threats_array = []
        business_threat_mitigations_array = []

        # Populate rows.
        for ans in answer.content:
            business_threats_array.append(ans['var_2'])
            business_threat_mitigations_array.append(ans['var_3'])

        # Generate our custom item.
        business_threats_dict = {
            "var": 'business_threats',
            'value': business_threats_array
        }
        business_threat_mitigations_dict = {
            "var": 'business_threat_mitigations',
            'value': business_threat_mitigations_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                business_threats_dict,
                business_threat_mitigations_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q151(self, answer, api):
        api.add_text(
            "product_distribution",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q153(self, answer, api):
        array = []

        if answer.content['var_1_other']:
            array.append(answer.content['var_1_other'])
        else:
            array.append(answer.content['var_1'])

        if answer.content['var_2_other']:
            array.append(answer.content['var_2_other'])
        else:
            array.append(answer.content['var_2'])

        if answer.content['var_3_other']:
            array.append(answer.content['var_3_other'])
        else:
            array.append(answer.content['var_3'])

        api.add_text_paragraphs('growth_strategies', array)

    def do_q154(self, answer, api):
        array = []

        if answer.content['var_1_other']:
            array.append(answer.content['var_1_other'])
        else:
            array.append(answer.content['var_1'])

        if answer.content['var_2_other']:
            array.append(answer.content['var_2_other'])
        else:
            array.append(answer.content['var_2'])

        if answer.content['var_3_other']:
            array.append(answer.content['var_3_other'])
        else:
            array.append(answer.content['var_3'])

        api.add_text_paragraphs('competitive_strategies', array)
