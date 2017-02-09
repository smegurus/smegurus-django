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
        api.add_text(
            "business_legal_structure",
            answer.content['var_1_other'] if answer.content['var_1_other'] else answer.content['var_1']
        )

    def do_q83(self, answer, api):
        api.add_text("business_st_address", answer.content['var_1'])
        api.add_text("business_city", answer.content['var_2'])
        api.add_text("business_country", answer.content['var_3'])
        api.add_text("business_province", answer.content['var_4'])

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
        col1_array = []
        col2_array = []
        col3_array = []
        col4_array = []

        # Populate rows.
        for ans in answer.content:
            col1_array.append(ans['title'])
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

    def do_q105(self, answer, api):
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
            "var": 'advisor_names',
            'value': col1_array
        }
        c2_dict = {
            "var": 'advisor_company_names',
            'value': col2_array
        }
        c3_dict = {
            "var": 'advisor_roles',
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

        api.add_text_paragraphs('competitive_strategies', array)
