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
from foundation_tenant.utils import humanize_number, humanize_currency
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
            if answer.question.pk == 25:  # naics_industry_name, naics_industry_friendly_name
                api.do_q25(answer, api)

            elif answer.question.pk == 27:  # business_idea
                api.do_q27(answer, api)

            elif answer.question.pk == 32:  # product_categories
                api.do_q32(answer, api)

            elif answer.question.pk == 44:  # industry_competition_levels
                api.do_q44(answer, api)

            # dc_names
            # dc_proximities
            # dc_market_shares
            # dc_price_comparisons
            # dc_main_strengths
            # dc_service_levels
            # dc_competitive_strategy
            elif answer.question.pk == 47:
                api.do_q47(answer, api)

            # idc_names
            # idc_proximities
            # idc_market_shares
            # idc_price_comparisons
            # idc_main_strengths
            # idc_service_levels
            # idc_competitive_strategy
            elif answer.question.pk == 48:
                api.do_q48(answer, api)

            # target_market_types
            # target_market_first_traits
            # target_market_second_traits
            elif answer.question.pk == 49:
                api.do_q49(answer, api)

            elif answer.question.pk == 61:  # business_formal_name, business_friendly_name
                api.do_q61(answer, api)

            elif answer.question.pk == 62:  # business_weaknesses, business_weakness_resolutions
                api.do_q62(answer, api)

            elif answer.question.pk == 63:  # business_mission
                api.do_q63(answer, api)

            elif answer.question.pk == 64:  # business_vision
                api.do_q64(answer, api)

            elif answer.question.pk == 65:  # product_customer_need
                api.do_q65(answer, api)

            elif answer.question.pk == 66:  # business_how_different
                api.do_q66(answer, api)

            elif answer.question.pk == 67:  # market_position, market_position_details
                api.do_q67(answer, api)

            elif answer.question.pk == 68:  # business_great_at
                api.do_q68(answer, api)

            elif answer.question.pk == 69:  # pricing_strategy
                api.do_q69(answer, api)

            elif answer.question.pk == 70:  # how_customer_buys
                api.do_q70(answer, api)

            elif answer.question.pk == 71:  # distribution_challenge
                api.do_q71(answer, api)

            elif answer.question.pk == 72:  # key_success_factors
                api.do_q72(answer, api)

            elif answer.question.pk == 74:  # how_to_convince
                api.do_q74(answer, api)

            elif answer.question.pk == 75:  # customer_objections, customer_objection_responses
                api.do_q75(answer, api)

            elif answer.question.pk == 76:  # customer_buying_time
                api.do_q76(answer, api)

            # incentive_types
            # incentive_impacts
            # incentive_durations
            # incentive_cost_types
            # incentive_y1_costs
            # incentive_y2_costs
            # incentive_y3_costs
            elif answer.question.pk == 77:
                items_array = []
                for item in answer.content:
                    item['var_6'] = humanize_currency(item['var_6'])
                    item['var_7'] = humanize_currency(item['var_7'])
                    item['var_8'] = humanize_currency(item['var_8'])
                    items_array.append(item)
                answer.content = items_array
                api.do_q77(answer, api)

            # physical_marketing_types
            # physical_marketing_impacts
            # physical_marketing_uses
            # physical_marketing_cost_types
            # physical_marketing_y1_costs
            # physical_marketing_y2_costs
            # physical_marketing_y3_costs
            elif answer.question.pk == 78:
                items_array = []
                for item in answer.content:
                    item['var_6'] = humanize_currency(item['var_6'])
                    item['var_7'] = humanize_currency(item['var_7'])
                    item['var_8'] = humanize_currency(item['var_8'])
                    items_array.append(item)
                answer.content = items_array
                api.do_q78(answer, api)

            # media_campaign_types
            # media_campaign_impacts
            # media_campaign_durations
            # media_campaign_cost_types
            # media_campaign_y1_costs
            # media_campaign_y2_costs
            # media_campaign_y3_costs
            elif answer.question.pk == 79:
                items_array = []
                for item in answer.content:
                    item['var_6'] = humanize_currency(item['var_6'])
                    item['var_7'] = humanize_currency(item['var_7'])
                    item['var_8'] = humanize_currency(item['var_8'])
                    items_array.append(item)
                answer.content = items_array
                api.do_q79(answer, api)

            # marketing_partnership_types
            # marketing_partnership_impacts
            # marketing_partnership_durations
            # marketing_partnership_cost_types
            # marketing_partnership_y1_costs
            # marketing_partnership_y2_costs
            # marketing_partnership_y3_costs
            elif answer.question.pk == 80:
                items_array = []
                for item in answer.content:
                    item['var_7'] = humanize_currency(item['var_7'])
                    item['var_8'] = humanize_currency(item['var_8'])
                    item['var_9'] = humanize_currency(item['var_9'])
                    items_array.append(item)
                answer.content = items_array
                api.do_q80(answer, api)

            elif answer.question.pk == 104:  # marketing_costs
                api.do_q104(answer, api)

            # marketing_referral_types
            # marketing_referral_impacts
            # marketing_referral_cost_types
            # marketing_referral_y1_costs
            # marketing_referral_y2_costs
            # marketing_referral_y3_costs
            elif answer.question.pk == 142:
                items_array = []
                for item in answer.content:
                    item['var_5'] = humanize_currency(item['var_5'])
                    item['var_6'] = humanize_currency(item['var_6'])
                    item['var_7'] = humanize_currency(item['var_7'])
                    items_array.append(item)
                answer.content = items_array
                api.do_q142(answer, api)

            # marketing_retention_types
            # marketing_retention_impacts
            # marketing_retention_cost_types
            # marketing_retention_y1_costs
            # marketing_retention_y2_costs
            # marketing_retention_y3_costs
            elif answer.question.pk == 143:
                items_array = []
                for item in answer.content:
                    item['var_5'] = humanize_currency(item['var_5'])
                    item['var_6'] = humanize_currency(item['var_6'])
                    item['var_7'] = humanize_currency(item['var_7'])
                    items_array.append(item)
                answer.content = items_array
                api.do_q143(answer, api)

            elif answer.question.pk == 147:  # business_strengths, business_strengths_1
                api.do_q147(answer, api)

            elif answer.question.pk == 148:  # business_opportunities
                api.do_q148(answer, api)

            elif answer.question.pk == 149:  # business_threats, business_threat_mitigations
                api.do_q149(answer, api)

            elif answer.question.pk == 151:  # product_distribution
                api.do_q151(answer, api)

            elif answer.question.pk == 153:  # growth_strategies
                api.do_q153(answer, api)

            elif answer.question.pk == 154:  # competitive_strategies
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
