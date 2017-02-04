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

        return #TODO: DELETE WHEN READY.

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
        return QuestionAnswer.objects.filter(
            Q(
                workspace_id=workspace_id,
                document__document_type__stage_num=7
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
            name="workspace_" + str(workspace.id) + "_stage_07",
            format="odt",
            template="templates/stage7.odt"
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
        today = timezone.now()
        api.add_text("date", str(today)) # date

        for answer in answers.all():
            if answer.question.pk == 27: # business_idea
                self.do_q27(answer, api)

            elif answer.question.pk == 61:
                # business_formal_name, business_friendly_name
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

            elif answer.question.pk == 153:
                self.do_q153(answer, api)

            elif answer.question.pk == 154:
                self.do_q154(answer, api)

    def do_q27(self, answer, api):
        api.add_text("business_idea", answer.content['var_1'])

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

        # --- Debugging purposes only. ---
        # print(custom)

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
        # 69	7	{{pricing_strategy}}
        print("QID 69") #TODO: IMPLEMENT

    def do_q70(self, answer, api):
        # 70	7	{{how_customer_buys}}
        print("QID 70") #TODO: IMPLEMENT

    def do_q71(self, answer, api):
        # 71	7	{{distribution_challenge}}
        # 71	7	{{distribution_challenge_resolution}}
        print("QID 71") #TODO: IMPLEMENT

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

    def do_q75(self, answer, api):
        # 75	7	{{customer_objections}}
        # 75	7	{{customer_objection_responses}}
        print("QID 75") #TODO: IMPLEMENT

    def do_q76(self, answer, api):
        # 76	7	"{{customer_buying_time}}
        print("QID 76") #TODO: IMPLEMENT

    def do_q77(self, answer, api):
        # 77	7	{{incentive_types}}
        # 77	7	{{incentive_impacts}}
        # 77	7	{{incentive_durations}}
        # 77	7	{{incentive_cost_types}}
        # 77	7	{{incentive_y1_costs}}
        # 77	7	{{incentive_y2_costs}}
        # 77	7	{{incentive_y3_costs}}
        print("QID 77") #TODO: IMPLEMENT

    def do_q78(self, answer, api):
        # 78	7	{{physical_marketing_types}}
        # 78	7	{{physical_marketing_impacts}}
        # 78	7	{{physical_marketing_uses}}
        # 78	7	{{physical_marketing_cost_types}}
        # 78	7	{{physical_marketing_y1_costs}}
        # 78	7	{{physical_marketing_y2_costs}}
        # 78	7	{{physical_marketing_y3_costs}}
        print("QID 78") #TODO: IMPLEMENT

    def do_q79(self, answer, api):
        # 79	7	{{media_campaign_types}}
        # 79	7	{{media_campaign_impacts}}
        # 79	7	{{media_campaign_durations}}
        # 79	7	{{media_campaign_cost_types}}
        # 79	7	{{media_campaign_y1_costs}}
        # 79	7	{{media_campaign_y2_costs}}
        # 79	7	{{media_campaign_y3_costs}}
        print("QID 79") #TODO: IMPLEMENT

    def do_q80(self, answer, api):
        # 80	7	{{marketing_partnership_types}}
        # 80	7	{{marketing_partnership_impacts}}
        # 80	7	{{marketing_partnership_durations}}
        # 80	7	{{marketing_partnership_cost_types}}
        # 80	7	{{marketing_partnership_y1_costs}}
        # 80	7	{{marketing_partnership_y2_costs}}
        # 80	7	{{marketing_partnership_y3_costs}}
        print("QID 80") #TODO: IMPLEMENT

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
        # 142	7	{{marketing_referral_types}}
        # 142	7	{{marketing_referral_impacts}}
        # 142	7	{{marketing_referral_cost_types}}
        # 142	7	{{marketing_referral_y1_costs}}
        # 142	7	{{marketing_referral_y2_costs}}
        # 142	7	{{marketing_referral_y3_costs}}
        print("QID 142") #TODO: IMPLEMENT

    def do_q143(self, answer, api):
        # 143	7	{{marketing_retention_types}}
        # 143	7	{{marketing_retention_impacts}}
        # 143	7	{{marketing_retention_cost_types}}
        # 143	7	{{marketing_retention_y1_costs}}
        # 143	7	{{marketing_retention_y2_costs}}
        # 143	7	{{marketing_retention_y3_costs}}
        print("QID 143") #TODO: IMPLEMENT

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

        # --- Debugging purposes only. ---
        # print(custom)

        # Attach all out tables.
        api.add_custom(custom)

    def do_q153(self, answer, api):
        print(answer.content)
        # 153	7	{{growth_strategies}}
        print("QID 153") #TODO: IMPLEMENT

    def do_q154(self, answer, api):
        # 154	7	{{competitive_strategies}}
        print("QID 154") #TODO: IMPLEMENT
