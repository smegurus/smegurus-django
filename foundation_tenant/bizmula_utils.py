from django.utils.translation import ugettext_lazy as _
from foundation_tenant.docxpresso_utils import DocxspressoAPI
from foundation_tenant.models.base.naicsoption import NAICSOption


class BizmulaAPI(DocxspressoAPI):
    """
    Class overrides the Docxpresso API and provides convinence functions
    for processing questions in the Bizmula Engine.
    """
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

    def do_q21(self, answer, api):
        api.add_text("workspace_name", answer.content['var_1'])
        api.add_text_to_footer("workspace_name", answer.content['var_1'])

    def do_q25(self, answer, api):
        naics_id = answer.content['var_5'] # Depth 5 NAICS ID
        depth_five_naics = NAICSOption.objects.get(id=naics_id) # Get the name
        api.add_text("naics_industry_name", depth_five_naics.name)
        api.add_text("naics_industry_friendly_name", answer.content['var_6'])

    def do_q26(self, answer, api):
        api.add_text("years_of_exp", answer.content['var_1'])

    def do_q27(self, answer, api):
        api.add_text("business_idea", answer.content['var_1'])

    def do_q28(self, answer, api):
        arr = []
        if answer.content['var_1_other']:
            arr.append(answer.content['var_1_other'])
        else:
            if answer.content['var_1']:
                arr.append(answer.content['var_1'])

        if answer.content['var_2_other']:
            arr.append(answer.content['var_2_other'])
        else:
            if answer.content['var_2']:
                arr.append(answer.content['var_2'])

        if answer.content['var_3_other']:
            arr.append(answer.content['var_3_other'])
        else:
            if answer.content['var_3']:
                arr.append(answer.content['var_3'])

        if answer.content['var_4_other']:
            arr.append(answer.content['var_4_other'])
        else:
            if answer.content['var_4']:
                arr.append(answer.content['var_4'])

        if answer.content['var_5_other']:
            arr.append(answer.content['var_5_other'])
        else:
            if answer.content['var_5']:
                arr.append(answer.content['var_5'])

        api.add_text_list("research_sources", arr)

    def do_q29(self, answer, api):
        arr = []
        arr.append(answer.content['var_1'])
        arr.append(answer.content['var_2'])
        arr.append(answer.content['var_3'])
        api.add_text_list("similar_businesses", arr)

    def do_q30(self, answer, api):
        arr = []
        arr.append(answer.content['var_1'])
        arr.append(answer.content['var_2'])
        arr.append(answer.content['var_3'])
        api.add_text_list("industry_contacts", arr)


    # def do_q32(self, answer, api):
    #     array = [
    #         answer.content['var_1'],
    #         answer.content['var_2'],
    #         answer.content['var_3']
    #     ];
    #     api.add_text_paragraphs("product_categories", array)

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
        api.add_text_paragraphs("pestel_trends", array)

    def do_q38(self, answer, api):
        array = []
        for ans in answer.content:
            array.append(ans['var_2'])
        api.add_text_paragraphs("specific_sources", array)

    def do_q39(self, answer, api):
        api.add_text(
            "geographic_market",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q40(self, answer, api): # customer_buying_decision | geographic_market
        # Compute the answer.
        var_1 = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']

        # Add our result.
        api.add_text(
            "customer_buying_decision",
            '-' if answer.content['var_0'] else var_1
        )

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

    def do_q49(self, answer, api):
        array = []
        for ans in answer.content:
            array.append(ans['var_2'] + " - " + ans['var_3'] + " - " + ans['var_4'])
        api.add_text_paragraphs("target_market_characteristics", array)

    def do_q52(self, answer, api):
        api.add_text(
            "customers_will_purchase",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q51(self, answer, api):
        api.add_text(
            "customer_price_sensitivity",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q54(self, answer, api):
        api.add_text(
            "test_reach_method",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q53(self, answer, api):
        api.add_text(
            "test_contact_number",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q55(self, answer, api):
        api.add_text(
            "test_contact_agreed",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q56(self, answer, api):
        api.add_text(
            "actual_contact_number",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q58(self, q58_answer, api, answers):
        # Find the other answer to compare to.
        q56_value = 0
        for answer in answers.all():
            if answer.question.pk == 56:
                q56_value = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']

        # Find the other value.
        q58_value = q58_answer.content['var_1_other'] if q58_answer.content['var_1_other'] else q58_answer.content['var_1']

        # # Debugging purposes only.
        # print("QID56", q56_value)
        # print("QID58", q58_value)

        # Decision computation.
        value = "Yes" if q58_value >= q56_value else "No"

        # # Debugging purposes only.
        # print("QID58 >= QID56 is", value)

        # Record our decision.
        api.add_text("validation_outcome_met", value)

        # Record another value.
        api.add_text("actual_supported_number", q56_value)

    def do_q59(self, answer, api):
        api.add_text("validation_lessons_learned",answer.content['var_1'])


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

    def do_q73(self, answer, api):
        array = []

        # Attach all the checkboxes.
        for ans in answer.content['var_1']:
            array.append(ans['value'])

        # Attach the other textfield.
        if answer.content['var_1_other']:
            array.append(answer.content['var_1_other'])

        # Attach our data to document.
        api.add_text_paragraphs("test_contact_method", array)

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
        self.do_type43(
            answer,
            api,
            'incentive_types',
            'incentive_impacts',
            'incentive_durations',
            'incentive_cost_types',
            'incentive_y1_costs',
            'incentive_y2_costs',
            'incentive_y3_costs',
        )

    def do_q78(self, answer, api):
        self.do_type43(
            answer,
            api,
            'physical_marketing_types',
            'physical_marketing_impacts',
            'physical_marketing_uses',
            'physical_marketing_cost_types',
            'physical_marketing_y1_costs',
            'physical_marketing_y2_costs',
            'physical_marketing_y3_costs',
        )

    def do_q79(self, answer, api):
        self.do_type43(
            answer,
            api,
            'media_campaign_types',
            'media_campaign_impacts',
            'media_campaign_durations',
            'media_campaign_cost_types',
            'media_campaign_y1_costs',
            'media_campaign_y2_costs',
            'media_campaign_y3_costs',
        )

    def do_q80(self, answer, api):
        self.do_type43(
            answer,
            api,
            'marketing_partnership_types',
            'marketing_partnership_impacts',
            'marketing_partnership_durations',
            'marketing_partnership_cost_types',
            'marketing_partnership_y1_costs',
            'marketing_partnership_y2_costs',
            'marketing_partnership_y3_costs',
        )

    def do_q81(self, answer, api):
        col1_array = []
        col2_array = []
        col3_array = []

        # Populate rows.
        for ans in answer.content:
            col1_array.append(ans['var_2'])
            col2_array.append(ans['var_3'])
            col3_array.append(ans['var_4'])

        # Generate our custom item.
        col1_dict = {
            "var": 'owner_names',
            'value': col1_array
        }
        col2_dict = {
            "var": 'owner_percentages',
            'value': col2_array
        }
        col3_dict = {
            "var": 'owner_types',
            'value': col3_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                col1_dict,
                col2_dict,
                col3_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q82(self, answer, api):
        api.add_text("business_legal_structure", answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1'])

    def do_q83(self, answer, api):
        api.add_text("business_st_address", answer.content['var_1'])
        api.add_text("business_city", answer.content['var_2'])
        api.add_text("business_country", answer.content['var_3'])
        api.add_text("business_province", answer.content['var_4'])

    def do_q84(self, answer, api):
        col1_array = []
        col2_array = []

        # Populate rows.
        for ans in answer.content:
            col1_array.append(ans['var_2'])
            col2_array.append(ans['var_3'])

        # Generate our custom item.
        c1_dict = {"var": 'business_space_uses', 'value': col1_array}
        c2_dict = {"var": 'business_sqft_sizes', 'value': col2_array}

        # Generate the custom API query.
        custom = {
            "vars": [
                c1_dict,
                c2_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q85(self, answer, api):
        self.do_type50(
            answer,
            api,
            'pro_fee_types',
            'pro_fee_details',
            'pro_fee_cost_types',
            'pro_fee_y1_costs',
            'pro_fee_y2_costs',
            'pro_fee_y3_costs'
        )

    def do_q86(self, answer, api):
        self.do_type50(
            answer,
            api,
            'location_cost_types',
            'location_details',
            'location_cost_types',
            'location_y1_costs',
            'location_y2_costs',
            'location_y3_costs'
        )

    def do_q87(self, answer, api):
        product_categories_array = []
        category_1_products_array = []

        # Populate rows.
        for ans in answer.content:
            product_categories_array.append(ans['var_2'])
            category_1_products_array.append(ans['var_3'])

        # Generate our custom item.
        product_categories_dict = {
            "var": 'product_categories',
            'value': product_categories_array
        }
        category_1_product_dict = {
            "var": 'category_1_products',
            'value': category_1_products_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                product_categories_dict,
                category_1_product_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q88(self, answer, api):
        api.add_text(
            "business_verb",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q89(self, answer, api):
        api.add_text(
            "customer_terms",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q90(self, answer, api):
        self.do_type50(
            answer,
            api,
            'license_types',
            'license_processes',
            'license_complete_percents',
            'license_y1_costs',
            'license_y2_costs',
            'license_y3_costs'
        )

    def do_q91(self, answer, api):
        col1_array = []
        col2_array = []
        col3_array = []

        # Populate rows.
        for ans in answer.content:
            col1_array.append(ans['var_2'])
            col2_array.append(ans['var_3'])
            col3_array.append(ans['var_4'])

        # Generate our custom item.
        c1_dict = {
            "var": 'management_names',
            'value': col1_array
        }
        c2_dict = {
            "var": 'management_roles',
            'value': col2_array
        }
        c3_dict = {
            "var": 'management_expertises',
            'value': col3_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                c1_dict,
                c2_dict,
                c3_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q92(self, answer, api):
        api.add_text(
            "management_strength_1",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )
        api.add_text(
            "management_strength_2",
            answer.content['var_2_other'] if answer.content['var_2_other'] else answer.content['var_2']
        )
        api.add_text(
            "management_strength_3",
            answer.content['var_3_other'] if answer.content['var_3_other'] else answer.content['var_3']
        )

    def do_q93(self, answer, api):
        col1_array = []
        col2_array = []

        # Populate rows.
        for ans in answer.content:
            col1_array.append(ans['var_2'])
            col2_array.append(ans['var_3'])
        # Generate our custom item.
        c1_dict = {
            "var": 'management_weaknesses',
            'value': col1_array
        }
        c2_dict = {
            "var": 'management_weakness_resolutions',
            'value': col2_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                c1_dict,
                c2_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q95(self, answer, api):
        self.do_type43(
            answer,
            api,
            'milestone_names',
            'milestone_risks',
            'milestone_persons',
            'milestone_starts',
            'milestone_ends',
            'milestone_costs',
            'milestone_completions'
        )

    def do_q97(self, answer, api):
        api.add_text(
            "cogs_are_you",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q98(self, answer, api):
        api.add_text(
            "cogs_how_to_forecast",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q99(self, answer, api):
        api.add_text("unit_sales_m1", answer.content['m1'])
        api.add_text("unit_sales_m2", answer.content['m2'])
        api.add_text("unit_sales_m3", answer.content['m3'])
        api.add_text("unit_sales_m4", answer.content['m4'])
        api.add_text("unit_sales_m5", answer.content['m5'])
        api.add_text("unit_sales_m6", answer.content['m6'])
        api.add_text("unit_sales_m7", answer.content['m7'])
        api.add_text("unit_sales_m8", answer.content['m8'])
        api.add_text("unit_sales_m9", answer.content['m9'])
        api.add_text("unit_sales_m10", answer.content['m10'])
        api.add_text("unit_sales_m11", answer.content['m11'])
        api.add_text("unit_sales_m12", answer.content['m12'])
        api.add_text("unit_sales_y1_total", answer.content['yr1_total'])
        api.add_text("unit_sales_m13", answer.content['m13'])
        api.add_text("unit_sales_m14", answer.content['m14'])
        api.add_text("unit_sales_m15", answer.content['m15'])
        api.add_text("unit_sales_m16", answer.content['m16'])
        api.add_text("unit_sales_m17", answer.content['m17'])
        api.add_text("unit_sales_m18", answer.content['m18'])
        api.add_text("unit_sales_m19", answer.content['m19'])
        api.add_text("unit_sales_m20", answer.content['m20'])
        api.add_text("unit_sales_m21", answer.content['m21'])
        api.add_text("unit_sales_m22", answer.content['m22'])
        api.add_text("unit_sales_m23", answer.content['m23'])
        api.add_text("unit_sales_m24", answer.content['m24'])
        api.add_text("unit_sales_y2_total", answer.content['yr2_total'])
        api.add_text("unit_sales_m25", answer.content['m25'])
        api.add_text("unit_sales_m26", answer.content['m26'])
        api.add_text("unit_sales_m27", answer.content['m27'])
        api.add_text("unit_sales_m28", answer.content['m28'])
        api.add_text("unit_sales_m29", answer.content['m29'])
        api.add_text("unit_sales_m30", answer.content['m30'])
        api.add_text("unit_sales_m31", answer.content['m31'])
        api.add_text("unit_sales_m32", answer.content['m32'])
        api.add_text("unit_sales_m33", answer.content['m33'])
        api.add_text("unit_sales_m34", answer.content['m34'])
        api.add_text("unit_sales_m35", answer.content['m35'])
        api.add_text("unit_sales_m36", answer.content['m36'])
        api.add_text("unit_sales_y3_total", answer.content['yr3_total'])

    def do_q100(self, answer, api):
        api.add_text("cogs_labour_year1", answer.content['labour_yr1'])
        api.add_text("cogs_labour_year2", answer.content['labour_yr2'])
        api.add_text("cogs_labour_year3", answer.content['labour_yr3'])

        api.add_text("cogs_material_year1", answer.content['materials_yr1'])
        api.add_text("cogs_material_year2", answer.content['materials_yr2'])
        api.add_text("cogs_material_year3", answer.content['materials_yr3'])

        api.add_text("cogs_materials_year1", answer.content['materials_yr1'])
        api.add_text("cogs_materials_year2", answer.content['materials_yr2'])
        api.add_text("cogs_materials_year3", answer.content['materials_yr3'])

        api.add_text("cogs_overhead_year1", answer.content['overhead_yr1'])
        api.add_text("cogs_overhead_year2", answer.content['overhead_yr2'])
        api.add_text("cogs_overhead_year3", answer.content['overhead_yr3'])

        api.add_text("total_cogs_year1", answer.content['total_cogs_yr1'])
        api.add_text("total_cogs_year2", answer.content['total_cogs_yr2'])
        api.add_text("total_cogs_year3", answer.content['total_cogs_yr3'])

        api.add_text("sales_price_per_unit_year1", answer.content['sales_per_unit_yr1'])
        api.add_text("sales_price_per_unit_year2", answer.content['sales_per_unit_yr2'])
        api.add_text("sales_price_per_unit_year3", answer.content['sales_per_unit_yr3'])

        api.add_text("gross_margin_percent_year1", answer.content['profit_percent_yr1'])
        api.add_text("gross_margin_percent_year2", answer.content['profit_percent_yr2'])
        api.add_text("gross_margin_percent_year3", answer.content['profit_percent_yr3'])
        api.add_text("gross_margin_dollars_year1", answer.content['profit_amount_yr1'])
        api.add_text("gross_margin_dollars_year2", answer.content['profit_amount_yr2'])
        api.add_text("gross_margin_dollars_year3", answer.content['profit_amount_yr3'])

    def do_q101(self, answer, api):
        api.add_text("cogs_materials_m1", answer.content['materials_month_1_other'] if answer.content['materials_month_1_other'] else answer.content['materials_month_1'])
        api.add_text("cogs_materials_m2", answer.content['materials_month_2_other'] if answer.content['materials_month_2_other'] else answer.content['materials_month_2'])
        api.add_text("cogs_materials_m3", answer.content['materials_month_3_other'] if answer.content['materials_month_3_other'] else answer.content['materials_month_3'])
        api.add_text("cogs_materials_m4", answer.content['materials_month_4_other'] if answer.content['materials_month_4_other'] else answer.content['materials_month_4'])
        api.add_text("cogs_materials_m5", answer.content['materials_month_5_other'] if answer.content['materials_month_5_other'] else answer.content['materials_month_5'])
        api.add_text("cogs_materials_m6", answer.content['materials_month_6_other'] if answer.content['materials_month_6_other'] else answer.content['materials_month_6'])
        api.add_text("cogs_materials_m7", answer.content['materials_month_7_other'] if answer.content['materials_month_7_other'] else answer.content['materials_month_7'])
        api.add_text("cogs_materials_m8", answer.content['materials_month_8_other'] if answer.content['materials_month_8_other'] else answer.content['materials_month_8'])
        api.add_text("cogs_materials_m9", answer.content['materials_month_9_other'] if answer.content['materials_month_9_other'] else answer.content['materials_month_9'])
        api.add_text("cogs_materials_m10", answer.content['materials_month_10_other'] if answer.content['materials_month_10_other'] else answer.content['materials_month_10'])
        api.add_text("cogs_materials_m11", answer.content['materials_month_11_other'] if answer.content['materials_month_11_other'] else answer.content['materials_month_11'])
        api.add_text("cogs_materials_m12", answer.content['materials_month_12_other'] if answer.content['materials_month_12_other'] else answer.content['materials_month_12'])
        # api.add_text("cogs_materials_y1_total", answer.content['materials_month_12_other'] if answer.content['materials_month_12_other'] else answer.content['materials_month_12'])

        api.add_text("cogs_materials_m13", answer.content['materials_month_13_other'] if answer.content['materials_month_1_other'] else answer.content['materials_month_13'])
        api.add_text("cogs_materials_m14", answer.content['materials_month_14_other'] if answer.content['materials_month_2_other'] else answer.content['materials_month_14'])
        api.add_text("cogs_materials_m15", answer.content['materials_month_15_other'] if answer.content['materials_month_3_other'] else answer.content['materials_month_15'])
        api.add_text("cogs_materials_m16", answer.content['materials_month_16_other'] if answer.content['materials_month_4_other'] else answer.content['materials_month_16'])
        api.add_text("cogs_materials_m17", answer.content['materials_month_17_other'] if answer.content['materials_month_5_other'] else answer.content['materials_month_17'])
        api.add_text("cogs_materials_m18", answer.content['materials_month_18_other'] if answer.content['materials_month_6_other'] else answer.content['materials_month_18'])
        api.add_text("cogs_materials_m19", answer.content['materials_month_19_other'] if answer.content['materials_month_7_other'] else answer.content['materials_month_19'])
        api.add_text("cogs_materials_m20", answer.content['materials_month_20_other'] if answer.content['materials_month_8_other'] else answer.content['materials_month_20'])
        api.add_text("cogs_materials_m21", answer.content['materials_month_21_other'] if answer.content['materials_month_9_other'] else answer.content['materials_month_21'])
        api.add_text("cogs_materials_m22", answer.content['materials_month_22_other'] if answer.content['materials_month_10_other'] else answer.content['materials_month_22'])
        api.add_text("cogs_materials_m23", answer.content['materials_month_23_other'] if answer.content['materials_month_11_other'] else answer.content['materials_month_23'])
        api.add_text("cogs_materials_m24", answer.content['materials_month_24_other'] if answer.content['materials_month_12_other'] else answer.content['materials_month_24'])
        # api.add_text("cogs_materials_y1_total", answer.content['materials_month_12_other'] if answer.content['materials_month_12_other'] else answer.content['materials_month_12'])

        api.add_text("cogs_materials_m25", answer.content['materials_month_25_other'] if answer.content['materials_month_25_other'] else answer.content['materials_month_25'])
        api.add_text("cogs_materials_m26", answer.content['materials_month_26_other'] if answer.content['materials_month_26_other'] else answer.content['materials_month_26'])
        api.add_text("cogs_materials_m27", answer.content['materials_month_27_other'] if answer.content['materials_month_27_other'] else answer.content['materials_month_27'])
        api.add_text("cogs_materials_m28", answer.content['materials_month_28_other'] if answer.content['materials_month_28_other'] else answer.content['materials_month_28'])
        api.add_text("cogs_materials_m29", answer.content['materials_month_29_other'] if answer.content['materials_month_29_other'] else answer.content['materials_month_29'])
        api.add_text("cogs_materials_m30", answer.content['materials_month_30_other'] if answer.content['materials_month_30_other'] else answer.content['materials_month_30'])
        api.add_text("cogs_materials_m31", answer.content['materials_month_31_other'] if answer.content['materials_month_31_other'] else answer.content['materials_month_31'])
        api.add_text("cogs_materials_m32", answer.content['materials_month_32_other'] if answer.content['materials_month_32_other'] else answer.content['materials_month_32'])
        api.add_text("cogs_materials_m33", answer.content['materials_month_33_other'] if answer.content['materials_month_33_other'] else answer.content['materials_month_33'])
        api.add_text("cogs_materials_m34", answer.content['materials_month_34_other'] if answer.content['materials_month_34_other'] else answer.content['materials_month_34'])
        api.add_text("cogs_materials_m35", answer.content['materials_month_35_other'] if answer.content['materials_month_35_other'] else answer.content['materials_month_35'])
        api.add_text("cogs_materials_m36", answer.content['materials_month_36_other'] if answer.content['materials_month_36_other'] else answer.content['materials_month_36'])
        # api.add_text("cogs_materials_y1_total", answer.content['materials_month_12_other'] if answer.content['materials_month_12_other'] else answer.content['materials_month_12'])

        api.add_text("cogs_labour_m1", answer.content['labour_month_1_other'] if answer.content['labour_month_1_other'] else answer.content['labour_month_1'])
        api.add_text("cogs_labour_m2", answer.content['labour_month_2_other'] if answer.content['labour_month_2_other'] else answer.content['labour_month_2'])
        api.add_text("cogs_labour_m3", answer.content['labour_month_3_other'] if answer.content['labour_month_3_other'] else answer.content['labour_month_3'])
        api.add_text("cogs_labour_m4", answer.content['labour_month_4_other'] if answer.content['labour_month_4_other'] else answer.content['labour_month_4'])
        api.add_text("cogs_labour_m5", answer.content['labour_month_5_other'] if answer.content['labour_month_5_other'] else answer.content['labour_month_5'])
        api.add_text("cogs_labour_m6", answer.content['labour_month_6_other'] if answer.content['labour_month_6_other'] else answer.content['labour_month_6'])
        api.add_text("cogs_labour_m7", answer.content['labour_month_7_other'] if answer.content['labour_month_7_other'] else answer.content['labour_month_7'])
        api.add_text("cogs_labour_m8", answer.content['labour_month_8_other'] if answer.content['labour_month_8_other'] else answer.content['labour_month_8'])
        api.add_text("cogs_labour_m9", answer.content['labour_month_9_other'] if answer.content['labour_month_9_other'] else answer.content['labour_month_9'])
        api.add_text("cogs_labour_m10", answer.content['labour_month_10_other'] if answer.content['labour_month_10_other'] else answer.content['labour_month_10'])
        api.add_text("cogs_labour_m11", answer.content['labour_month_11_other'] if answer.content['labour_month_11_other'] else answer.content['labour_month_11'])
        api.add_text("cogs_labour_m12", answer.content['labour_month_12_other'] if answer.content['labour_month_12_other'] else answer.content['labour_month_12'])
        # api.add_text("cogs_labour_y1_total", answer.content['labour_month_12_other'] if answer.content['labour_month_12_other'] else answer.content['labour_month_12'])

        api.add_text("cogs_labour_m13", answer.content['labour_month_13_other'] if answer.content['labour_month_1_other'] else answer.content['labour_month_13'])
        api.add_text("cogs_labour_m14", answer.content['labour_month_14_other'] if answer.content['labour_month_2_other'] else answer.content['labour_month_14'])
        api.add_text("cogs_labour_m15", answer.content['labour_month_15_other'] if answer.content['labour_month_3_other'] else answer.content['labour_month_15'])
        api.add_text("cogs_labour_m16", answer.content['labour_month_16_other'] if answer.content['labour_month_4_other'] else answer.content['labour_month_16'])
        api.add_text("cogs_labour_m17", answer.content['labour_month_17_other'] if answer.content['labour_month_5_other'] else answer.content['labour_month_17'])
        api.add_text("cogs_labour_m18", answer.content['labour_month_18_other'] if answer.content['labour_month_6_other'] else answer.content['labour_month_18'])
        api.add_text("cogs_labour_m19", answer.content['labour_month_19_other'] if answer.content['labour_month_7_other'] else answer.content['labour_month_19'])
        api.add_text("cogs_labour_m20", answer.content['labour_month_20_other'] if answer.content['labour_month_8_other'] else answer.content['labour_month_20'])
        api.add_text("cogs_labour_m21", answer.content['labour_month_21_other'] if answer.content['labour_month_9_other'] else answer.content['labour_month_21'])
        api.add_text("cogs_labour_m22", answer.content['labour_month_22_other'] if answer.content['labour_month_10_other'] else answer.content['labour_month_22'])
        api.add_text("cogs_labour_m23", answer.content['labour_month_23_other'] if answer.content['labour_month_11_other'] else answer.content['labour_month_23'])
        api.add_text("cogs_labour_m24", answer.content['labour_month_24_other'] if answer.content['labour_month_12_other'] else answer.content['labour_month_24'])
        # api.add_text("cogs_labour_y1_total", answer.content['labour_month_12_other'] if answer.content['labour_month_12_other'] else answer.content['labour_month_12'])

        api.add_text("cogs_labour_m25", answer.content['labour_month_25_other'] if answer.content['labour_month_25_other'] else answer.content['labour_month_25'])
        api.add_text("cogs_labour_m26", answer.content['labour_month_26_other'] if answer.content['labour_month_26_other'] else answer.content['labour_month_26'])
        api.add_text("cogs_labour_m27", answer.content['labour_month_27_other'] if answer.content['labour_month_27_other'] else answer.content['labour_month_27'])
        api.add_text("cogs_labour_m28", answer.content['labour_month_28_other'] if answer.content['labour_month_28_other'] else answer.content['labour_month_28'])
        api.add_text("cogs_labour_m29", answer.content['labour_month_29_other'] if answer.content['labour_month_29_other'] else answer.content['labour_month_29'])
        api.add_text("cogs_labour_m30", answer.content['labour_month_30_other'] if answer.content['labour_month_30_other'] else answer.content['labour_month_30'])
        api.add_text("cogs_labour_m31", answer.content['labour_month_31_other'] if answer.content['labour_month_31_other'] else answer.content['labour_month_31'])
        api.add_text("cogs_labour_m32", answer.content['labour_month_32_other'] if answer.content['labour_month_32_other'] else answer.content['labour_month_32'])
        api.add_text("cogs_labour_m33", answer.content['labour_month_33_other'] if answer.content['labour_month_33_other'] else answer.content['labour_month_33'])
        api.add_text("cogs_labour_m34", answer.content['labour_month_34_other'] if answer.content['labour_month_34_other'] else answer.content['labour_month_34'])
        api.add_text("cogs_labour_m35", answer.content['labour_month_35_other'] if answer.content['labour_month_35_other'] else answer.content['labour_month_35'])
        api.add_text("cogs_labour_m36", answer.content['labour_month_36_other'] if answer.content['labour_month_36_other'] else answer.content['labour_month_36'])
        # api.add_text("cogs_labour_y1_total", answer.content['labour_month_12_other'] if answer.content['labour_month_12_other'] else answer.content['labour_month_12'])

        api.add_text("cogs_overhead_m1", answer.content['overhead_month_1_other'] if answer.content['overhead_month_1_other'] else answer.content['overhead_month_1'])
        api.add_text("cogs_overhead_m2", answer.content['overhead_month_2_other'] if answer.content['overhead_month_2_other'] else answer.content['overhead_month_2'])
        api.add_text("cogs_overhead_m3", answer.content['overhead_month_3_other'] if answer.content['overhead_month_3_other'] else answer.content['overhead_month_3'])
        api.add_text("cogs_overhead_m4", answer.content['overhead_month_4_other'] if answer.content['overhead_month_4_other'] else answer.content['overhead_month_4'])
        api.add_text("cogs_overhead_m5", answer.content['overhead_month_5_other'] if answer.content['overhead_month_5_other'] else answer.content['overhead_month_5'])
        api.add_text("cogs_overhead_m6", answer.content['overhead_month_6_other'] if answer.content['overhead_month_6_other'] else answer.content['overhead_month_6'])
        api.add_text("cogs_overhead_m7", answer.content['overhead_month_7_other'] if answer.content['overhead_month_7_other'] else answer.content['overhead_month_7'])
        api.add_text("cogs_overhead_m8", answer.content['overhead_month_8_other'] if answer.content['overhead_month_8_other'] else answer.content['overhead_month_8'])
        api.add_text("cogs_overhead_m9", answer.content['overhead_month_9_other'] if answer.content['overhead_month_9_other'] else answer.content['overhead_month_9'])
        api.add_text("cogs_overhead_m10", answer.content['overhead_month_10_other'] if answer.content['overhead_month_10_other'] else answer.content['overhead_month_10'])
        api.add_text("cogs_overhead_m11", answer.content['overhead_month_11_other'] if answer.content['overhead_month_11_other'] else answer.content['overhead_month_11'])
        api.add_text("cogs_overhead_m12", answer.content['overhead_month_12_other'] if answer.content['overhead_month_12_other'] else answer.content['overhead_month_12'])
        # api.add_text("cogs_overhead_y1_total", answer.content['overhead_month_12_other'] if answer.content['overhead_month_12_other'] else answer.content['overhead_month_12'])

        api.add_text("cogs_overhead_m13", answer.content['overhead_month_13_other'] if answer.content['overhead_month_1_other'] else answer.content['overhead_month_13'])
        api.add_text("cogs_overhead_m14", answer.content['overhead_month_14_other'] if answer.content['overhead_month_2_other'] else answer.content['overhead_month_14'])
        api.add_text("cogs_overhead_m15", answer.content['overhead_month_15_other'] if answer.content['overhead_month_3_other'] else answer.content['overhead_month_15'])
        api.add_text("cogs_overhead_m16", answer.content['overhead_month_16_other'] if answer.content['overhead_month_4_other'] else answer.content['overhead_month_16'])
        api.add_text("cogs_overhead_m17", answer.content['overhead_month_17_other'] if answer.content['overhead_month_5_other'] else answer.content['overhead_month_17'])
        api.add_text("cogs_overhead_m18", answer.content['overhead_month_18_other'] if answer.content['overhead_month_6_other'] else answer.content['overhead_month_18'])
        api.add_text("cogs_overhead_m19", answer.content['overhead_month_19_other'] if answer.content['overhead_month_7_other'] else answer.content['overhead_month_19'])
        api.add_text("cogs_overhead_m20", answer.content['overhead_month_20_other'] if answer.content['overhead_month_8_other'] else answer.content['overhead_month_20'])
        api.add_text("cogs_overhead_m21", answer.content['overhead_month_21_other'] if answer.content['overhead_month_9_other'] else answer.content['overhead_month_21'])
        api.add_text("cogs_overhead_m22", answer.content['overhead_month_22_other'] if answer.content['overhead_month_10_other'] else answer.content['overhead_month_22'])
        api.add_text("cogs_overhead_m23", answer.content['overhead_month_23_other'] if answer.content['overhead_month_11_other'] else answer.content['overhead_month_23'])
        api.add_text("cogs_overhead_m24", answer.content['overhead_month_24_other'] if answer.content['overhead_month_12_other'] else answer.content['overhead_month_24'])
        # api.add_text("cogs_overhead_y1_total", answer.content['overhead_month_12_other'] if answer.content['overhead_month_12_other'] else answer.content['overhead_month_12'])

        api.add_text("cogs_overhead_m25", answer.content['overhead_month_25_other'] if answer.content['overhead_month_25_other'] else answer.content['overhead_month_25'])
        api.add_text("cogs_overhead_m26", answer.content['overhead_month_26_other'] if answer.content['overhead_month_26_other'] else answer.content['overhead_month_26'])
        api.add_text("cogs_overhead_m27", answer.content['overhead_month_27_other'] if answer.content['overhead_month_27_other'] else answer.content['overhead_month_27'])
        api.add_text("cogs_overhead_m28", answer.content['overhead_month_28_other'] if answer.content['overhead_month_28_other'] else answer.content['overhead_month_28'])
        api.add_text("cogs_overhead_m29", answer.content['overhead_month_29_other'] if answer.content['overhead_month_29_other'] else answer.content['overhead_month_29'])
        api.add_text("cogs_overhead_m30", answer.content['overhead_month_30_other'] if answer.content['overhead_month_30_other'] else answer.content['overhead_month_30'])
        api.add_text("cogs_overhead_m31", answer.content['overhead_month_31_other'] if answer.content['overhead_month_31_other'] else answer.content['overhead_month_31'])
        api.add_text("cogs_overhead_m32", answer.content['overhead_month_32_other'] if answer.content['overhead_month_32_other'] else answer.content['overhead_month_32'])
        api.add_text("cogs_overhead_m33", answer.content['overhead_month_33_other'] if answer.content['overhead_month_33_other'] else answer.content['overhead_month_33'])
        api.add_text("cogs_overhead_m34", answer.content['overhead_month_34_other'] if answer.content['overhead_month_34_other'] else answer.content['overhead_month_34'])
        api.add_text("cogs_overhead_m35", answer.content['overhead_month_35_other'] if answer.content['overhead_month_35_other'] else answer.content['overhead_month_35'])
        api.add_text("cogs_overhead_m36", answer.content['overhead_month_36_other'] if answer.content['overhead_month_36_other'] else answer.content['overhead_month_36'])
        # api.add_text("cogs_overhead_y1_total", answer.content['overhead_month_12_other'] if answer.content['overhead_month_12_other'] else answer.content['overhead_month_12'])

    def do_q102(self, answer, api):
        print("QID 102")

    def do_q103(self, answer, api):
        # Note: Cannot use "do_type41" function
        col1_array = []
        col2_array = []
        col3_array = []
        col4_array = []

        # Populate rows.
        for ans in answer.content:
            col1_array.append(ans['title']) # These need to be var_1, etc to support "do_type41".
            col2_array.append(ans['yr1_percent'])
            col3_array.append(ans['yr2_percent'])
            col4_array.append(ans['yr3_percent'])

        # Generate our custom item.
        col1_dict = {
            "var": 'target_market_types',
            'value': col1_array
        }
        col2_dict = {
            "var": 'sales_year1_targetmarkets',
            'value': col2_array
        }
        col3_dict = {
            "var": 'sales_year2_targetmarkets',
            'value': col3_array
        }
        col4_dict = {
            "var": 'sales_year3_targetmarkets',
            'value': col4_array
        }

        # Generate the custom API query.
        custom = {
            "vars": [
                col1_dict,
                col2_dict,
                col3_dict,
                col4_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_q104(self, answer, api):
        self.do_type52(answer, api, "marketing_costs")

    def do_q105(self, answer, api):
        self.do_type50(
            answer,
            api,
            'salary_types',
            'salary_details',
            'salary_cost_types',
            'salary_year1_costs',
            'salary_year2_costs',
            'salary_year3_costs'
        )

    def do_q106(self, answer, api):
        self.do_type52(answer, api, "salary_cost")

    def do_q107(self, answer, api):
        self.do_type52(answer, api, "pro_fee_cost")

    def do_q108(self, answer, api):
        self.do_type50(
            answer,
            api,
            'transportation_types',
            'transportation_details',
            'transportation_cost_types',
            'transportation_y1_costs',
            'transportation_y2_costs',
            'transportation_y3_costs'
        )

    def do_q109(self, answer, api):
        self.do_type52(answer, api, "transportation_costs")

    def do_q110(self, answer, api):
        self.do_type52(answer, api, "location_costs")

    def do_q111(self, answer, api):
        self.do_type50(
            answer,
            api,
            'admin_types',
            'admin_details',
            'admin_cost_types',
            'admin_y1_costs',
            'admin_y2_costs',
            'admin_y3_costs'
        )

    def do_q112(self, answer, api):
        self.do_type52(answer, api, "admin_cost")

    def do_q113(self, answer, api):
        self.do_type52(answer, api, "license_costs")

    def do_q114(self, answer, api):
        self.do_type50(
            answer,
            api,
            'insurance_types',
            'insurance_details',
            'insurance_cost_types',
            'insurance_y1_costs',
            'insurance_y2_costs',
            'insurance_y3_costs'
        )

    def do_q115(self, answer, api):
        self.do_type52(answer, api, "insurance_costs")

    def do_q116(self, answer, api):
        self.do_type50(
            answer,
            api,
            'bank_fee_types',
            'bank_fee_details',
            'bank_fee_cost_types',
            'bank_fee_y1_costs',
            'bank_fee_y2_costs',
            'bank_fee_y3_costs'
        )

    def do_q117(self, answer, api):
        self.do_type52(answer, api, "bank_fees")

    def do_q118(self, answer, api):
        yr1_total = 0
        yr2_total = 0
        yr3_total = 0

        # Populate rows.
        for ans in answer.content:
            yr1_total += self.string_to_float(ans['var_5'])
            yr2_total += self.string_to_float(ans['var_6'])
            yr3_total += self.string_to_float(ans['var_7'])

        # Populate the totals.
        api.add_text("supplies_costs_y1_total", yr1_total)
        api.add_text("supplies_costs_y2_total", yr2_total)
        api.add_text("supplies_costs_y3_total", yr3_total)

        # Populate the table.
        self.do_type50(
            answer,
            api,
            'supplies_types',
            'supplies_details',
            'supplies_cost_types',
            'supplies_y1_costs',
            'supplies_y2_costs',
            'supplies_y3_costs'
        )

    def do_q119(self, answer, api):
        self.do_type52(answer, api, "supplies_costs")

    def do_q120(self, answer, api):
        self.do_type50(
            answer,
            api,
            'comm_types',
            'comm_details',
            'comm_cost_types',
            'comm_y1_costs',
            'comm_y2_costs',
            'comm_y3_costs'
        )

    def do_q121(self, answer, api):
        self.do_type52(answer, api, "comm_costs")

    def do_q122(self, answer, api):
        self.do_type50(
            answer,
            api,
            'sub_types',
            'sub_details',
            'sub_cost_types',
            'sub_y1_costs',
            'sub_y2_costs',
            'sub_y3_costs'
        )

    def do_q123(self, answer, api):
        self.do_type52(answer, api, "sub_costs")

    def do_q124(self, answer, api):
        self.do_type50(
            answer,
            api,
            'sales_expense_types',
            'sales_expense_details',
            'sales_expense_cost_types',
            'sales_y1_costs',
            'sales_y2_costs',
            'sales_y3_costs'
        )

    def do_q125(self, answer, api):
        self.do_type52(answer, api, "sales_expense")

    def do_q126(self, answer, api):
        self.do_type50(
            answer,
            api,
            'mem_types',
            'mem_details',
            'mem_cost_types',
            'mem_y1_costs',
            'mem_y2_costs',
            'mem_y3_costs'
        )

    def do_q127(self, answer, api):
        self.do_type52(answer, api, "mem_costs")

    def do_q128(self, answer, api):
        self.do_type50(
            answer,
            api,
            'lease_types',
            'lease_details',
            'lease_cost_types',
            'lease_y1_costs',
            'lease_y2_costs',
            'lease_y3_costs'
        )

    def do_q129(self, answer, api):
        self.do_type52(answer, api, "lease_costs")

    def do_q130(self, answer, api):
        self.do_type50(
            answer,
            api,
            'maintain_types',
            'maintain_details',
            'maintain_cost_types',
            'maintain_y1_costs',
            'maintain_y2_costs',
            'maintain_y3_costs'
        )

    def do_q131(self, answer, api):
        self.do_type52(answer, api, "maintain_costs")

    def do_q132(self, answer, api):
        self.do_type50(
            answer,
            api,
            'other_types',
            'other_details',
            'other_cost_types',
            'other_y1_costs',
            'other_y2_costs',
            'other_y3_costs'
        )

    def do_q133(self, answer, api):
        self.do_type52(answer, api, "other_costs")

    def do_q134(self, answer, api):
        self.do_type50(
            answer,
            api,
            'misc_types',
            'misc_details',
            'misc_cost_types',
            'misc_y1_costs',
            'misc_y2_costs',
            'misc_y3_costs'
        )

    def do_q135(self, answer, api):
        self.do_type52(answer, api, "misc_costs")

    def do_q136(self, answer, api):
        yr1_total = 0
        yr2_total = 0
        yr3_total = 0

        # Populate rows.
        for ans in answer.content:
            yr1_total += self.string_to_float(ans['var_5'])
            yr2_total += self.string_to_float(ans['var_6'])
            yr3_total += self.string_to_float(ans['var_7'])

        # Populate "taxes_total".
        taxes_total = yr1_total + yr2_total + yr3_total
        api.add_text("depreciation_total", taxes_total)

        # # Populate the annual totals.
        api.add_text("depreciation_total_y1", yr1_total)
        api.add_text("depreciation_total_y2", yr2_total)
        api.add_text("depreciation_total_y3", yr3_total)

        # Populate the table.
        self.do_type50(
            answer,
            api,
            'asset_names',
            'asset_deps',
            'asset_cost_types',
            'asset_y1_costs',
            'asset_y2_costs',
            'asset_y3_costs'
        )

    def do_q137(self, answer, api):
        yr1_total = 0
        yr2_total = 0
        yr3_total = 0

        # Populate rows.
        for ans in answer.content:
            yr1_total += self.string_to_float(ans['var_5'])
            yr2_total += self.string_to_float(ans['var_6'])
            yr3_total += self.string_to_float(ans['var_7'])

        # Populate "taxes_total".
        taxes_total = yr1_total + yr2_total + yr3_total
        api.add_text("interest_total", taxes_total)

        # # Populate the annual totals.
        api.add_text("interest_total_y1", yr1_total)
        api.add_text("interest_total_y2", yr2_total)
        api.add_text("interest_total_y3", yr3_total)

        # Populate the table.
        self.do_type50(
            answer,
            api,
            'interest_items',
            'interest_details',
            'interest_cost_types',
            'interest_y1_costs',
            'interest_y2_costs',
            'interest_y3_costs'
        )

    def do_q138(self, answer, api):
        yr1_total = 0
        yr2_total = 0
        yr3_total = 0

        # Populate rows.
        for ans in answer.content:
            yr1_total += self.string_to_float(ans['var_5'])
            yr2_total += self.string_to_float(ans['var_6'])
            yr3_total += self.string_to_float(ans['var_7'])

        # Populate "taxes_total".
        taxes_total = yr1_total + yr2_total + yr3_total
        api.add_text("taxes_total", taxes_total)

        # # Populate the annual totals.
        api.add_text("taxes_total_y1", yr1_total)
        api.add_text("taxes_total_y2", yr2_total)
        api.add_text("taxes_total_y3", yr3_total)

        # Populate the tax table.
        self.do_type50(
            answer,
            api,
            'tax_items',
            'tax_details',
            'tax_cost_types',
            'tax_y1_costs',
            'tax_y2_costs',
            'tax_y3_costs'
        )

    def do_q136_q137_q138(self, qid_136_answer, qid_137_answer, qid_138_answer, api):
        yr1_total = 0
        yr2_total = 0
        yr3_total = 0

        # Populate rows.
        for ans in qid_136_answer.content:
            yr1_total += self.string_to_float(ans['var_5'])
            yr2_total += self.string_to_float(ans['var_6'])
            yr3_total += self.string_to_float(ans['var_7'])
        for ans in qid_137_answer.content:
            yr1_total += self.string_to_float(ans['var_5'])
            yr2_total += self.string_to_float(ans['var_6'])
            yr3_total += self.string_to_float(ans['var_7'])
        for ans in qid_138_answer.content:
            yr1_total += self.string_to_float(ans['var_5'])
            yr2_total += self.string_to_float(ans['var_6'])
            yr3_total += self.string_to_float(ans['var_7'])

        # total = yr1_total + yr2_total + yr3_total
        api.add_text("tid_total_y1", yr1_total)
        api.add_text("tid_total_y2", yr2_total)
        api.add_text("tid_total_y3", yr3_total)

    def do_q139(self, answer, api):
        self.do_type50(
            answer,
            api,
            'sales_expense_types',
            'sales_expense_details',
            'sales_expense_cost_types',
            'sales_y1_costs',
            'sales_y2_costs',
            'sales_y3_costs'
        )

    def do_q140(self, answer, api):
        self.do_type50(
            answer,
            api,
            'asset_items',
            'asset_types',
            'asset_details',
            'asset_y1_costs',
            'asset_y2_costs',
            'sales_y3_costs'
        )

    def do_q141(self, answer, api):
        api.add_text("months_startup_inventory", answer.content['var_1'])

    def do_q142(self, answer, api):
        self.do_type50(
            answer,
            api,
            'marketing_referral_types',
            'marketing_referral_impacts',
            'marketing_referral_cost_types',
            'marketing_referral_y1_costs',
            'marketing_referral_y2_costs',
            'marketing_referral_y3_costs'
        )

    def do_q143(self, answer, api):
        self.do_type50(
            answer,
            api,
            'marketing_retention_types',
            'marketing_retention_impacts',
            'marketing_retention_cost_types',
            'marketing_retention_y1_costs',
            'marketing_retention_y2_costs',
            'marketing_retention_y3_costs'
        )

    def do_q144(self, answer, api):
        # print(answer.content)
        api.add_text("low_rev_y1", answer.content['var_2']['revenue']['yr1'])
        api.add_text("low_rev_y2", answer.content['var_2']['revenue']['yr2'])
        api.add_text("low_rev_y3", answer.content['var_2']['revenue']['yr3'])
        api.add_text("low_cogs_y1", answer.content['var_2']['cogs']['yr1'])
        api.add_text("low_cogs_y2", answer.content['var_2']['cogs']['yr2'])
        api.add_text("low_cogs_y3", answer.content['var_2']['cogs']['yr3'])
        api.add_text("low_gp_y1", answer.content['var_2']['gross_profit']['yr1'])
        api.add_text("low_gp_y2", answer.content['var_2']['gross_profit']['yr2'])
        api.add_text("low_gp_y3", answer.content['var_2']['gross_profit']['yr3'])
        api.add_text("low_gp_percent_y1", answer.content['var_2']['gross_margin_percent']['yr1'])
        api.add_text("low_gp_percent_y2", answer.content['var_2']['gross_margin_percent']['yr2'])
        api.add_text("low_gp_percent_y3", answer.content['var_2']['gross_margin_percent']['yr3'])
        api.add_text("low_net_profit_y1", answer.content['var_2']['net_profit']['yr1'])
        api.add_text("low_net_profit_y2", answer.content['var_2']['net_profit']['yr2'])
        api.add_text("low_net_profit_y3", answer.content['var_2']['net_profit']['yr3'])
        api.add_text("low_net_profit_percent_y1", answer.content['var_2']['net_profit_percent']['yr1'])
        api.add_text("low_net_profit_percent_y2", answer.content['var_2']['net_profit_percent']['yr2'])
        api.add_text("low_net_profit_percent_y3", answer.content['var_2']['net_profit_percent']['yr3'])
        api.add_text("low_sales_y1", answer.content['var_2']['total_sales']['yr1'])
        api.add_text("low_sales_y2", answer.content['var_2']['total_sales']['yr2'])
        api.add_text("low_sales_y3", answer.content['var_2']['total_sales']['yr3'])
        api.add_text("low_cogs_labour_y1", answer.content['var_2']['labour']['yr1'])
        api.add_text("low_cogs_labour_y2", answer.content['var_2']['labour']['yr2'])
        api.add_text("low_cogs_labour_y3", answer.content['var_2']['labour']['yr3'])
        api.add_text("low_cogs_mat_y1", answer.content['var_2']['materials']['yr1'])
        api.add_text("low_cogs_mat_y2", answer.content['var_2']['materials']['yr2'])
        api.add_text("low_cogs_mat_y3", answer.content['var_2']['materials']['yr3'])
        api.add_text("low_cogs_oh_y1", answer.content['var_2']['overhead']['yr1'])
        api.add_text("low_cogs_oh_y2", answer.content['var_2']['overhead']['yr2'])
        api.add_text("low_cogs_oh_y3", answer.content['var_2']['overhead']['yr3'])
        api.add_text("low_tot_var_y1", answer.content['var_2']['total_variable_costs']['yr1'])
        api.add_text("low_tot_var_y2", answer.content['var_2']['total_variable_costs']['yr2'])
        api.add_text("low_tot_var_y3", answer.content['var_2']['total_variable_costs']['yr3'])
        api.add_text("low_tot_var_ex_cogs_y1", answer.content['var_2']['total_variable_costs_excluding_cogs']['yr1'])
        api.add_text("low_tot_var_ex_cogs_y2", answer.content['var_2']['total_variable_costs_excluding_cogs']['yr2'])
        api.add_text("low_tot_var_ex_cogs_y3", answer.content['var_2']['total_variable_costs_excluding_cogs']['yr3'])
        api.add_text("low_tot_fc_y1", answer.content['var_2']['total_fixed']['yr1'])
        api.add_text("low_tot_fc_y2", answer.content['var_2']['total_fixed']['yr2'])
        api.add_text("low_tot_fc_y3", answer.content['var_2']['total_fixed']['yr3'])
        api.add_text("low_gen_exp_y1", answer.content['var_2']['general_and_marketing_expenses']['yr1'])
        api.add_text("low_gen_exp_y2", answer.content['var_2']['general_and_marketing_expenses']['yr2'])
        api.add_text("low_gen_exp_y3", answer.content['var_2']['general_and_marketing_expenses']['yr3'])

    def do_q145(self, answer, api):
        # print(answer.content)
        api.add_text("hi_rev_y1", answer.content['var_2']['revenue']['yr1'])
        api.add_text("hi_rev_y2", answer.content['var_2']['revenue']['yr2'])
        api.add_text("hi_rev_y3", answer.content['var_2']['revenue']['yr3'])
        api.add_text("hi_cogs_y1", answer.content['var_2']['cogs']['yr1'])
        api.add_text("hi_cogs_y2", answer.content['var_2']['cogs']['yr2'])
        api.add_text("hi_cogs_y3", answer.content['var_2']['cogs']['yr3'])
        api.add_text("hi_gp_y1", answer.content['var_2']['gross_profit']['yr1'])
        api.add_text("hi_gp_y2", answer.content['var_2']['gross_profit']['yr2'])
        api.add_text("hi_gp_y3", answer.content['var_2']['gross_profit']['yr3'])
        api.add_text("hi_gp_percent_y1", answer.content['var_2']['gross_margin_percent']['yr1'])
        api.add_text("hi_gp_percent_y2", answer.content['var_2']['gross_margin_percent']['yr2'])
        api.add_text("hi_gp_percent_y3", answer.content['var_2']['gross_margin_percent']['yr3'])
        api.add_text("hi_net_profit_y1", answer.content['var_2']['net_profit']['yr1'])
        api.add_text("hi_net_profit_y2", answer.content['var_2']['net_profit']['yr2'])
        api.add_text("hi_net_profit_y3", answer.content['var_2']['net_profit']['yr3'])
        api.add_text("hi_net_profit_percent_y1", answer.content['var_2']['net_profit_percent']['yr1'])
        api.add_text("hi_net_profit_percent_y2", answer.content['var_2']['net_profit_percent']['yr2'])
        api.add_text("hi_net_profit_percent_y3", answer.content['var_2']['net_profit_percent']['yr3'])
        api.add_text("hi_sales_y1", answer.content['var_2']['total_sales']['yr1'])
        api.add_text("hi_sales_y2", answer.content['var_2']['total_sales']['yr2'])
        api.add_text("hi_sales_y3", answer.content['var_2']['total_sales']['yr3'])
        api.add_text("hi_cogs_labour_y1", answer.content['var_2']['labour']['yr1'])
        api.add_text("hi_cogs_labour_y2", answer.content['var_2']['labour']['yr2'])
        api.add_text("hi_cogs_labour_y3", answer.content['var_2']['labour']['yr3'])
        api.add_text("hi_cogs_mat_y1", answer.content['var_2']['materials']['yr1'])
        api.add_text("hi_cogs_mat_y2", answer.content['var_2']['materials']['yr2'])
        api.add_text("hi_cogs_mat_y3", answer.content['var_2']['materials']['yr3'])
        api.add_text("hi_cogs_oh_y1", answer.content['var_2']['overhead']['yr1'])
        api.add_text("hi_cogs_oh_y2", answer.content['var_2']['overhead']['yr2'])
        api.add_text("hi_cogs_oh_y3", answer.content['var_2']['overhead']['yr3'])
        api.add_text("hi_tot_var_y1", answer.content['var_2']['total_variable_costs']['yr1'])
        api.add_text("hi_tot_var_y2", answer.content['var_2']['total_variable_costs']['yr2'])
        api.add_text("hi_tot_var_y3", answer.content['var_2']['total_variable_costs']['yr3'])
        api.add_text("hi_tot_var_ex_cogs_y1", answer.content['var_2']['total_variable_costs_excluding_cogs']['yr1'])
        api.add_text("hi_tot_var_ex_cogs_y2", answer.content['var_2']['total_variable_costs_excluding_cogs']['yr2'])
        api.add_text("hi_tot_var_ex_cogs_y3", answer.content['var_2']['total_variable_costs_excluding_cogs']['yr3'])
        api.add_text("hi_tot_fc_y1", answer.content['var_2']['total_fixed']['yr1'])
        api.add_text("hi_tot_fc_y2", answer.content['var_2']['total_fixed']['yr2'])
        api.add_text("hi_tot_fc_y3", answer.content['var_2']['total_fixed']['yr3'])
        api.add_text("hi_gen_exp_y1", answer.content['var_2']['general_and_marketing_expenses']['yr1'])
        api.add_text("hi_gen_exp_y2", answer.content['var_2']['general_and_marketing_expenses']['yr2'])
        api.add_text("hi_gen_exp_y3", answer.content['var_2']['general_and_marketing_expenses']['yr3'])

    def do_q146(self, answer, api):
        # Convert
        value_str = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        value_str = value_str.replace('$', '')
        value_str = value_str.replace(',', '')
        value = float(value_str)

        # Input.
        api.add_text("ent_cash_req", value)
        api.add_text("ent_cash_req_6mths", value * 6.00)

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

    def do_q150(self, answer, api):
        text = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        api.add_text("industry_competition_amount", text)

    def do_q151(self, answer, api):
        api.add_text(
            "product_distribution",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q152(self, answer, api):
        text = answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        api.add_text("avg_customer_spending", text)

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

        api.add_text_paragraphs('location_benefits_1', array)

    def do_q155(self, answer, api):
        if answer.content['var_1_other']:
            api.add_text('location_benefits_1', answer.content['var_1_other'])
        else:
            api.add_text('location_benefits_1', answer.content['var_1'])

        if answer.content['var_2_other']:
            api.add_text('location_benefits_2', answer.content['var_2_other'])
        else:
            api.add_text('location_benefits_2', answer.content['var_2'])

        if answer.content['var_3_other']:
            api.add_text('location_benefits_3', answer.content['var_3_other'])
        else:
            api.add_text('location_benefits_3', answer.content['var_3'])

    def do_q156(self, answer, api):
        self.do_type43(
            answer,
            api,
            'suppliers_names',
            'supplier_products',
            'supplier_proximities',
            'supplier_terms',
            'supplier_price_levels',
            'supplier_strengths',
            'supplier_relationships'
        )

    def do_q157(self, answer, api):
        api.add_text(
            "bp_reason",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q158(self, answer, api):
        self.do_type41(
            answer,
            api,
            'fund_names',
            'fund_uses',
            'fund_impacts',
            'fund_amounts'
        )

    def do_q161(self, answer, api):
        api.add_picture('prod_image1', answer.content['var_3'])

    def do_q162(self, answer, api):
        api.add_picture('prod_image2', answer.content['var_3'])

    def do_type41(self, answer, api, key1, key2, key3, key4):  # 4 Col Table
        col1_array = []
        col2_array = []
        col3_array = []
        col4_array = []

        # Populate rows.
        for ans in answer.content:
            col1_array.append(ans['var_2'])
            col2_array.append(ans['var_3'])
            col3_array.append(ans['var_4'])
            col4_array.append(ans['var_5'])

        # Generate our custom item.
        c1_dict = {"var": key1, 'value': col1_array}
        c2_dict = {"var": key2, 'value': col2_array}
        c3_dict = {"var": key3, 'value': col3_array}
        c4_dict = {"var": key4, 'value': col4_array}

        # Generate the custom API query.
        custom = {
            "vars": [
                c1_dict,
                c2_dict,
                c3_dict,
                c4_dict
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

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
        c7_dict = {"var": key6, 'value': col7_array}

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

    def do_type50(self, answer, api, key1, key2, key3, key4, key5, key6):  # 6 Col Table
        col1_array = []
        col2_array = []
        col3_array = []
        col4_array = []
        col5_array = []
        col6_array = []

        # Populate rows.
        for ans in answer.content:
            col1_array.append(ans['var_2'])
            col2_array.append(ans['var_3'])
            col3_array.append(ans['var_4'])
            col4_array.append(ans['var_5'])
            col5_array.append(ans['var_6'])
            col6_array.append(ans['var_7'])

        # Generate our custom item.
        c1_dict = {"var": key1, 'value': col1_array}
        c2_dict = {"var": key2, 'value': col2_array}
        c3_dict = {"var": key3, 'value': col3_array}
        c4_dict = {"var": key4, 'value': col4_array}
        c5_dict = {"var": key5, 'value': col5_array}
        c6_dict = {"var": key6, 'value': col6_array}

        # Generate the custom API query.
        custom = {
            "vars": [
                c1_dict,
                c2_dict,
                c3_dict,
                c4_dict,
                c5_dict,
                c6_dict,
            ],
            "options": {
                "element": "table"
            }
        }

        # Attach all out tables.
        api.add_custom(custom)

    def do_type52(self, answer, api, prefix):
        api.add_text(prefix+"_m1", answer.content['m_01'] if answer.content['m_01'] else answer.content['m_01_r'])
        api.add_text(prefix+"_m2", answer.content['m_02'] if answer.content['m_02'] else answer.content['m_02_r'])
        api.add_text(prefix+"_m3", answer.content['m_03'] if answer.content['m_03'] else answer.content['m_03_r'])
        api.add_text(prefix+"_m4", answer.content['m_04'] if answer.content['m_04'] else answer.content['m_04_r'])
        api.add_text(prefix+"_m5", answer.content['m_05'] if answer.content['m_05'] else answer.content['m_05_r'])
        api.add_text(prefix+"_m6", answer.content['m_06'] if answer.content['m_06'] else answer.content['m_06_r'])
        api.add_text(prefix+"_m7", answer.content['m_07'] if answer.content['m_07'] else answer.content['m_07_r'])
        api.add_text(prefix+"_m8", answer.content['m_08'] if answer.content['m_08'] else answer.content['m_08_r'])
        api.add_text(prefix+"_m9", answer.content['m_09'] if answer.content['m_09'] else answer.content['m_09_r'])
        api.add_text(prefix+"_m10", answer.content['m_10'] if answer.content['m_10'] else answer.content['m_10_r'])
        api.add_text(prefix+"_m11", answer.content['m11'] if answer.content['m_11'] else answer.content['m_11_r'])
        api.add_text(prefix+"_m12", answer.content['m12'] if answer.content['m_12'] else answer.content['m_12_r'])
        api.add_text(prefix+"_y1_total", answer.content['yr_1'] if answer.content['yr_1'] else answer.content['yr_1_r'])
        api.add_text(prefix+"_m13", answer.content['m_13'] if answer.content['m_13'] else answer.content['m_13_r'])
        api.add_text(prefix+"_m14", answer.content['m_14'] if answer.content['m_14'] else answer.content['m_14_r'])
        api.add_text(prefix+"_m15", answer.content['m_15'] if answer.content['m_15'] else answer.content['m_15_r'])
        api.add_text(prefix+"_m16", answer.content['m_16'] if answer.content['m_16'] else answer.content['m_16_r'])
        api.add_text(prefix+"_m17", answer.content['m_17'] if answer.content['m_17'] else answer.content['m_17_r'])
        api.add_text(prefix+"_m18", answer.content['m_18'] if answer.content['m_18'] else answer.content['m_18_r'])
        api.add_text(prefix+"_m19", answer.content['m_19'] if answer.content['m_19'] else answer.content['m_19_r'])
        api.add_text(prefix+"_m20", answer.content['m_20'] if answer.content['m_20'] else answer.content['m_20_r'])
        api.add_text(prefix+"_m21", answer.content['m_21'] if answer.content['m_21'] else answer.content['m_21_r'])
        api.add_text(prefix+"_m22", answer.content['m_22'] if answer.content['m_22'] else answer.content['m_22_r'])
        api.add_text(prefix+"_m23", answer.content['m_23'] if answer.content['m_23'] else answer.content['m_23_r'])
        api.add_text(prefix+"_m24", answer.content['m_24'] if answer.content['m_24'] else answer.content['m_24_r'])
        api.add_text(prefix+"_y2_total", answer.content['yr_1'] if answer.content['yr_2'] else answer.content['yr_2_r'])
        api.add_text(prefix+"_m25", answer.content['m_25'] if answer.content['m_25'] else answer.content['m_25_r'])
        api.add_text(prefix+"_m26", answer.content['m_26'] if answer.content['m_26'] else answer.content['m_26_r'])
        api.add_text(prefix+"_m27", answer.content['m_27'] if answer.content['m_27'] else answer.content['m_27_r'])
        api.add_text(prefix+"_m28", answer.content['m_28'] if answer.content['m_28'] else answer.content['m_28_r'])
        api.add_text(prefix+"_m29", answer.content['m_29'] if answer.content['m_29'] else answer.content['m_29_r'])
        api.add_text(prefix+"_m30", answer.content['m_30'] if answer.content['m_30'] else answer.content['m_30_r'])
        api.add_text(prefix+"_m31", answer.content['m_31'] if answer.content['m_31'] else answer.content['m_31_r'])
        api.add_text(prefix+"_m32", answer.content['m_32'] if answer.content['m_32'] else answer.content['m_32_r'])
        api.add_text(prefix+"_m33", answer.content['m_33'] if answer.content['m_33'] else answer.content['m_33_r'])
        api.add_text(prefix+"_m34", answer.content['m_34'] if answer.content['m_34'] else answer.content['m_34_r'])
        api.add_text(prefix+"_m35", answer.content['m_35'] if answer.content['m_35'] else answer.content['m_35_r'])
        api.add_text(prefix+"_m36", answer.content['m_36'] if answer.content['m_36'] else answer.content['m_36_r'])
        api.add_text(prefix+"_y3_total", answer.content['yr_3'] if answer.content['yr_3'] else answer.content['yr_3_r'])

    def string_to_float(self, string):
        string = string.replace('$', '')
        string = string.replace(',', '')
        return float(string)
