# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from foundation_tenant.utils import int_or_none
from foundation_tenant.models.base.naicsoption import NAICSOption
from foundation_tenant.models.base.imageupload import TenantImageUpload
from foundation_tenant.models.bizmula.question import Question
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer
from smegurus import constants


register = template.Library()  # Register our custom template tag.


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def get_processed_row(data, key):
    """
    Utility function will pick either the custom overriden value or the default
    value for the row.
    """
    if data[key+'_r']:
        return data[key+'_r']
    else:
        return data[key]


def get_processed_table(data):
    """
    Utility function for taking a table and picking the custom overriden values
    or the default values for the entire table.
    """
    return {
        # Year 1
        'm_01':  get_processed_row(data, 'm_01'),
        'm_02':  get_processed_row(data, 'm_02'),
        'm_03':  get_processed_row(data, 'm_03'),
        'm_04':  get_processed_row(data, 'm_04'),
        'm_05':  get_processed_row(data, 'm_05'),
        'm_06':  get_processed_row(data, 'm_06'),
        'm_07':  get_processed_row(data, 'm_07'),
        'm_08':  get_processed_row(data, 'm_08'),
        'm_09':  get_processed_row(data, 'm_09'),
        'm_10':  get_processed_row(data, 'm_10'),
        'm_11':  get_processed_row(data, 'm_11'),
        'm_12':  get_processed_row(data, 'm_12'),
        'yr_1':  get_processed_row(data, 'yr_1'),

        # Year 2
        'm_13':  get_processed_row(data, 'm_13'),
        'm_14':  get_processed_row(data, 'm_14'),
        'm_15':  get_processed_row(data, 'm_15'),
        'm_16':  get_processed_row(data, 'm_16'),
        'm_17':  get_processed_row(data, 'm_17'),
        'm_18':  get_processed_row(data, 'm_18'),
        'm_19':  get_processed_row(data, 'm_19'),
        'm_20':  get_processed_row(data, 'm_20'),
        'm_21':  get_processed_row(data, 'm_21'),
        'm_22':  get_processed_row(data, 'm_22'),
        'm_23':  get_processed_row(data, 'm_23'),
        'm_24':  get_processed_row(data, 'm_24'),
        'yr_2':  get_processed_row(data, 'yr_2'),

        # Year 3
        'm_25':  get_processed_row(data, 'm_25'),
        'm_26':  get_processed_row(data, 'm_26'),
        'm_27':  get_processed_row(data, 'm_27'),
        'm_28':  get_processed_row(data, 'm_28'),
        'm_29':  get_processed_row(data, 'm_29'),
        'm_30':  get_processed_row(data, 'm_30'),
        'm_31':  get_processed_row(data, 'm_31'),
        'm_32':  get_processed_row(data, 'm_32'),
        'm_33':  get_processed_row(data, 'm_33'),
        'm_34':  get_processed_row(data, 'm_34'),
        'm_35':  get_processed_row(data, 'm_35'),
        'm_36':  get_processed_row(data, 'm_36'),
        'yr_1':  get_processed_row(data, 'yr_1')
    }


def get_table_for_qid(workspace, qid):
    """
    Utility function will get the (processed) table data for the yr1, yr2, yr3
    table answer.
    """
    answer = QuestionAnswer.objects.get(
        question_id=qid,
        workspace=workspace
    )
    return get_processed_table(answer.content)


def get_table_for_qid_163(workspace, q19_qid):
    q19 = QuestionAnswer.objects.get(
        question_id=q19_qid,
        workspace=workspace
    )
    q19 = q19.content
    return {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'total_sales_m1': q19['m1'], 'total_sales_m2': q19['m2'], 'total_sales_m3': q19['m3'],
        'total_sales_m4': q19['m4'], 'total_sales_m5': q19['m5'], 'total_sales_m6': q19['m6'],
        'total_sales_m7': q19['m7'], 'total_sales_m8': q19['m8'], 'total_sales_m9': q19['m9'],
        'total_sales_m10': q19['m10'], 'total_sales_m11': q19['m11'], 'total_sales_m12': q19['m12'],
        'total_sales_y1': q19['yr1_total'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'total_sales_m13': q19['m13'], 'total_sales_m14': q19['m14'], 'total_sales_m15': q19['m15'],
        'total_sales_m16': q19['m16'], 'total_sales_m17': q19['m17'], 'total_sales_m18': q19['m18'],
        'total_sales_m19': q19['m19'], 'total_sales_m20': q19['m20'], 'total_sales_m21': q19['m21'],
        'total_sales_m22': q19['m22'], 'total_sales_m23': q19['m23'], 'total_sales_m24': q19['m24'],
        'total_sales_y2': q19['yr2_total'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'total_sales_m25': q19['m25'], 'total_sales_m26': q19['m26'], 'total_sales_m27': q19['m27'],
        'total_sales_m28': q19['m28'], 'total_sales_m29': q19['m29'], 'total_sales_m30': q19['m30'],
        'total_sales_m31': q19['m31'], 'total_sales_m32': q19['m32'], 'total_sales_m33': q19['m33'],
        'total_sales_m34': q19['m34'], 'total_sales_m35': q19['m35'], 'total_sales_m36': q19['m36'],
        'total_sales_y3': q19['yr3_total'],
    }

def get_table_for_qid_101(workspace, qid):
    """
    Utility function will get the (processed) table data for the yr1, yr2, yr3
    table answer.
    """
    answer = QuestionAnswer.objects.get(
        question_id=qid,
        workspace=workspace
    )
    total_cogs = answer.content
    return {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'total_cogs_m1': total_cogs['total_month_1_other'] if total_cogs['total_month_1_other'] else total_cogs['total_month_1'],
        'total_cogs_m2': total_cogs['total_month_2_other'] if total_cogs['total_month_2_other'] else total_cogs['total_month_2'],
        'total_cogs_m3': total_cogs['total_month_3_other'] if total_cogs['total_month_3_other'] else total_cogs['total_month_3'],
        'total_cogs_m4': total_cogs['total_month_4_other'] if total_cogs['total_month_4_other'] else total_cogs['total_month_4'],
        'total_cogs_m5': total_cogs['total_month_5_other'] if total_cogs['total_month_5_other'] else total_cogs['total_month_5'],
        'total_cogs_m6': total_cogs['total_month_6_other'] if total_cogs['total_month_6_other'] else total_cogs['total_month_6'],
        'total_cogs_m7': total_cogs['total_month_7_other'] if total_cogs['total_month_7_other'] else total_cogs['total_month_7'],
        'total_cogs_m8': total_cogs['total_month_8_other'] if total_cogs['total_month_8_other'] else total_cogs['total_month_8'],
        'total_cogs_m9': total_cogs['total_month_9_other'] if total_cogs['total_month_9_other'] else total_cogs['total_month_9'],
        'total_cogs_m10': total_cogs['total_month_10_other'] if total_cogs['total_month_10_other'] else total_cogs['total_month_10'],
        'total_cogs_m11': total_cogs['total_month_11_other'] if total_cogs['total_month_11_other'] else total_cogs['total_month_11'],
        'total_cogs_m12': total_cogs['total_month_12_other'] if total_cogs['total_month_12_other'] else total_cogs['total_month_12'],
        'total_cogs_y1': total_cogs['total_year_1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'total_cogs_m13': total_cogs['total_month_13_other'] if total_cogs['total_month_13_other'] else total_cogs['total_month_13'],
        'total_cogs_m14': total_cogs['total_month_14_other'] if total_cogs['total_month_14_other'] else total_cogs['total_month_14'],
        'total_cogs_m15': total_cogs['total_month_15_other'] if total_cogs['total_month_15_other'] else total_cogs['total_month_15'],
        'total_cogs_m16': total_cogs['total_month_16_other'] if total_cogs['total_month_16_other'] else total_cogs['total_month_16'],
        'total_cogs_m17': total_cogs['total_month_17_other'] if total_cogs['total_month_17_other'] else total_cogs['total_month_17'],
        'total_cogs_m18': total_cogs['total_month_18_other'] if total_cogs['total_month_18_other'] else total_cogs['total_month_18'],
        'total_cogs_m19': total_cogs['total_month_19_other'] if total_cogs['total_month_19_other'] else total_cogs['total_month_19'],
        'total_cogs_m20': total_cogs['total_month_20_other'] if total_cogs['total_month_20_other'] else total_cogs['total_month_20'],
        'total_cogs_m21': total_cogs['total_month_21_other'] if total_cogs['total_month_21_other'] else total_cogs['total_month_21'],
        'total_cogs_m22': total_cogs['total_month_22_other'] if total_cogs['total_month_22_other'] else total_cogs['total_month_22'],
        'total_cogs_m23': total_cogs['total_month_23_other'] if total_cogs['total_month_23_other'] else total_cogs['total_month_23'],
        'total_cogs_m24': total_cogs['total_month_24_other'] if total_cogs['total_month_24_other'] else total_cogs['total_month_24'],
        'total_cogs_y2': total_cogs['total_year_2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'total_cogs_m25': total_cogs['total_month_25_other'] if total_cogs['total_month_25_other'] else total_cogs['total_month_25'],
        'total_cogs_m26': total_cogs['total_month_26_other'] if total_cogs['total_month_26_other'] else total_cogs['total_month_26'],
        'total_cogs_m27': total_cogs['total_month_27_other'] if total_cogs['total_month_27_other'] else total_cogs['total_month_27'],
        'total_cogs_m28': total_cogs['total_month_28_other'] if total_cogs['total_month_28_other'] else total_cogs['total_month_28'],
        'total_cogs_m29': total_cogs['total_month_29_other'] if total_cogs['total_month_29_other'] else total_cogs['total_month_29'],
        'total_cogs_m30': total_cogs['total_month_30_other'] if total_cogs['total_month_30_other'] else total_cogs['total_month_30'],
        'total_cogs_m31': total_cogs['total_month_31_other'] if total_cogs['total_month_31_other'] else total_cogs['total_month_31'],
        'total_cogs_m32': total_cogs['total_month_32_other'] if total_cogs['total_month_32_other'] else total_cogs['total_month_32'],
        'total_cogs_m33': total_cogs['total_month_33_other'] if total_cogs['total_month_33_other'] else total_cogs['total_month_33'],
        'total_cogs_m34': total_cogs['total_month_34_other'] if total_cogs['total_month_34_other'] else total_cogs['total_month_34'],
        'total_cogs_m35': total_cogs['total_month_35_other'] if total_cogs['total_month_35_other'] else total_cogs['total_month_35'],
        'total_cogs_m36': total_cogs['total_month_36_other'] if total_cogs['total_month_36_other'] else total_cogs['total_month_36'],
        'total_cogs_y3': total_cogs['total_year_3']
    }


def get_profit_margine(total_sales, total_cogs):
    return {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'gross_profit_m1': total_sales['total_sales_m1'] - total_cogs['total_cogs_m1'],
        'gross_profit_m2': total_sales['total_sales_m2'] - total_cogs['total_cogs_m2'],
        'gross_profit_m3': total_sales['total_sales_m3'] - total_cogs['total_cogs_m3'],
        'gross_profit_m4': total_sales['total_sales_m4'] - total_cogs['total_cogs_m4'],
        'gross_profit_m5': total_sales['total_sales_m5'] - total_cogs['total_cogs_m5'],
        'gross_profit_m6': total_sales['total_sales_m6'] - total_cogs['total_cogs_m6'],
        'gross_profit_m7': total_sales['total_sales_m7'] - total_cogs['total_cogs_m7'],
        'gross_profit_m8': total_sales['total_sales_m8'] - total_cogs['total_cogs_m8'],
        'gross_profit_m9': total_sales['total_sales_m9'] - total_cogs['total_cogs_m9'],
        'gross_profit_m10': total_sales['total_sales_m10'] - total_cogs['total_cogs_m10'],
        'gross_profit_m11': total_sales['total_sales_m11'] - total_cogs['total_cogs_m11'],
        'gross_profit_m12': total_sales['total_sales_m12'] - total_cogs['total_cogs_m12'],
        'gross_profit_yr1': total_sales['total_sales_y1'] - total_cogs['total_cogs_y1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'gross_profit_m13': total_sales['total_sales_m13'] - total_cogs['total_cogs_m13'],
        'gross_profit_m14': total_sales['total_sales_m14'] - total_cogs['total_cogs_m14'],
        'gross_profit_m15': total_sales['total_sales_m15'] - total_cogs['total_cogs_m15'],
        'gross_profit_m16': total_sales['total_sales_m16'] - total_cogs['total_cogs_m16'],
        'gross_profit_m17': total_sales['total_sales_m17'] - total_cogs['total_cogs_m17'],
        'gross_profit_m18': total_sales['total_sales_m18'] - total_cogs['total_cogs_m18'],
        'gross_profit_m19': total_sales['total_sales_m19'] - total_cogs['total_cogs_m19'],
        'gross_profit_m20': total_sales['total_sales_m20'] - total_cogs['total_cogs_m20'],
        'gross_profit_m21': total_sales['total_sales_m21'] - total_cogs['total_cogs_m21'],
        'gross_profit_m22': total_sales['total_sales_m22'] - total_cogs['total_cogs_m22'],
        'gross_profit_m23': total_sales['total_sales_m23'] - total_cogs['total_cogs_m23'],
        'gross_profit_m24': total_sales['total_sales_m24'] - total_cogs['total_cogs_m24'],
        'gross_profit_yr2': total_sales['total_sales_y2'] - total_cogs['total_cogs_y2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'gross_profit_m25': total_sales['total_sales_m25'] - total_cogs['total_cogs_m25'],
        'gross_profit_m26': total_sales['total_sales_m26'] - total_cogs['total_cogs_m26'],
        'gross_profit_m27': total_sales['total_sales_m27'] - total_cogs['total_cogs_m27'],
        'gross_profit_m28': total_sales['total_sales_m28'] - total_cogs['total_cogs_m28'],
        'gross_profit_m29': total_sales['total_sales_m29'] - total_cogs['total_cogs_m29'],
        'gross_profit_m30': total_sales['total_sales_m30'] - total_cogs['total_cogs_m30'],
        'gross_profit_m31': total_sales['total_sales_m31'] - total_cogs['total_cogs_m31'],
        'gross_profit_m32': total_sales['total_sales_m32'] - total_cogs['total_cogs_m32'],
        'gross_profit_m33': total_sales['total_sales_m33'] - total_cogs['total_cogs_m33'],
        'gross_profit_m34': total_sales['total_sales_m34'] - total_cogs['total_cogs_m34'],
        'gross_profit_m35': total_sales['total_sales_m35'] - total_cogs['total_cogs_m35'],
        'gross_profit_m36': total_sales['total_sales_m36'] - total_cogs['total_cogs_m36'],
        'gross_profit_yr3': total_sales['total_sales_y3'] - total_cogs['total_cogs_y3']
    }


@register.inclusion_tag('templatetags/question/template_067.html')
def render_question_type_067(workspace, module, node, question, answer):
    #================================#
    # Fetch & pre-process questions. #
    #================================#

    # PK 101 - total_cogs_m1
    q1_qid = int_or_none(question.dependency['q1_qid'])
    total_cogs = get_table_for_qid_101(workspace, q1_qid)

    # PK 104 - Stage 7, Marketing Costs
    q2_qid = int_or_none(question.dependency['q2_qid'])
    marketing_costs = get_table_for_qid(workspace, q2_qid)

    # PK 108 - Salaries
    q3_qid = int_or_none(question.dependency['q3_qid'])
    q3 = QuestionAnswer.objects.get(
        question_id=q3_qid,
        workspace=workspace
    )
    q3 = q3.content
    total_yr1 = 0.0
    total_yr2 = 0.0
    total_yr3 = 0.0
    for item in q3:
        total_yr1 += float(item['var_5'])
        total_yr2 += float(item['var_6'])
        total_yr3 += float(item['var_7'])
    salaries = {
        'yr1': total_yr1,
        'yr2': total_yr2,
        'yr3': total_yr3
    }

    # PK107 - Pro Fees
    q4_qid = int_or_none(question.dependency['q4_qid'])
    pro_fees = get_table_for_qid(workspace, q4_qid)

    # PK112 - Admin. costs
    q5_qid = int_or_none(question.dependency['q5_qid'])
    admin_costs = get_table_for_qid(workspace, q5_qid)

    # PK125 - Sales expenses
    q6_qid = int_or_none(question.dependency['q6_qid'])
    sales_expenses = get_table_for_qid(workspace, q6_qid)

    # PK110 - Location specific costs
    q7_qid = int_or_none(question.dependency['q7_qid'])
    loc_specific_costs = get_table_for_qid(workspace, q7_qid)

    # PK115 - Insurance costs
    q8_qid = int_or_none(question.dependency['q8_qid'])
    insurance_costs = get_table_for_qid(workspace, q8_qid)

    # PK113 - License/Registration costs
    q9_qid = int_or_none(question.dependency['q9_qid'])
    license_reg_costs = get_table_for_qid(workspace, q9_qid)

    # PK109 - Transportation costs
    q10_qid = int_or_none(question.dependency['q10_qid'])
    transportation_costs = get_table_for_qid(workspace, q10_qid)

    # PK117 - Banking costs
    q11_qid = int_or_none(question.dependency['q11_qid'])
    banking_costs = get_table_for_qid(workspace, q11_qid)

    # PK119 - Office supplies
    q12_qid = int_or_none(question.dependency['q12_qid'])
    office_supplies_cost = get_table_for_qid(workspace, q12_qid)

    # PK121 - Communication Costs
    q13_qid = int_or_none(question.dependency['q13_qid'])
    communication_costs = get_table_for_qid(workspace, q13_qid)

    # PK127 - Membership fees
    q14_qid = int_or_none(question.dependency['q14_qid'])
    membership_fees = get_table_for_qid(workspace, q14_qid)

    # PK129 - Equipment lease
    q15_qid = int_or_none(question.dependency['q15_qid'])
    equipment_lease = get_table_for_qid(workspace, q15_qid)

    # PK131 - Maintenance
    q16_qid = int_or_none(question.dependency['q16_qid'])
    maintain_costs = get_table_for_qid(workspace, q16_qid)

    # PK133 - Other
    q17_qid = int_or_none(question.dependency['q17_qid'])
    other_costs = get_table_for_qid(workspace, q17_qid)

    # PK135 - Misc
    q18_qid = int_or_none(question.dependency['q18_qid'])
    misc_costs = get_table_for_qid(workspace, q18_qid)

    # PK163 - total_sales_m1
    q19_qid = int_or_none(question.dependency['q19_qid'])
    total_sales = get_table_for_qid_163(workspace, q19_qid)

    # PK167 - net_startup_deficit_surplus
    q20_qid = int_or_none(question.dependency['q20_qid'])
    q20 = QuestionAnswer.objects.get(
        question_id=q20_qid,
        workspace=workspace
    )
    q20 = q20.content

    #====================================#
    # Pre-Process question computations. #
    #====================================#
    gross_profit = get_profit_margine(total_sales, total_cogs)

    #================================#
    # Process question computations. #
    #================================#
    computation = {} # Variable to store our table.

    # Start-up Costs
    #------------------------

    # Start-Up Surplus/Deficit
    computation = merge_two_dicts(computation, {
        'net_startup_deficit_surplus': q20['net_startup_deficit_surplus'],
    })

    # Revenue
    #------------------------
    computation = merge_two_dicts(computation, total_sales)
    computation = merge_two_dicts(computation, total_cogs)
    computation = merge_two_dicts(computation, gross_profit)

    # General & Admin Expenses
    #------------------------
    computation = merge_two_dicts(computation, {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'location_costs_m1': loc_specific_costs['m_01'], 'location_costs_m2': loc_specific_costs['m_02'], 'location_costs_m3': loc_specific_costs['m_03'],
        'location_costs_m4': loc_specific_costs['m_04'], 'location_costs_m5': loc_specific_costs['m_05'], 'location_costs_m6': loc_specific_costs['m_06'],
        'location_costs_m7': loc_specific_costs['m_07'], 'location_costs_m8': loc_specific_costs['m_08'], 'location_costs_m9': loc_specific_costs['m_09'],
        'location_costs_m10': loc_specific_costs['m_10'], 'location_costs_m11': loc_specific_costs['m_11'], 'location_costs_m12': loc_specific_costs['m_12'],
        'location_costs_yr1': loc_specific_costs['yr_1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'location_costs_m13': loc_specific_costs['m_13'], 'location_costs_m14': loc_specific_costs['m_14'], 'location_costs_m15': loc_specific_costs['m_15'],
        'location_costs_m16': loc_specific_costs['m_16'], 'location_costs_m17': loc_specific_costs['m_17'], 'location_costs_m18': loc_specific_costs['m_18'],
        'location_costs_m19': loc_specific_costs['m_19'], 'location_costs_m20': loc_specific_costs['m_20'], 'location_costs_m21': loc_specific_costs['m_21'],
        'location_costs_m22': loc_specific_costs['m_22'], 'location_costs_m23': loc_specific_costs['m_23'], 'location_costs_m24': loc_specific_costs['m_24'],
        'location_costs_yr2': loc_specific_costs['yr_2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'location_costs_m25': loc_specific_costs['m_25'], 'location_costs_m26': loc_specific_costs['m_26'], 'location_costs_m27': loc_specific_costs['m_27'],
        'location_costs_m28': loc_specific_costs['m_28'], 'location_costs_m29': loc_specific_costs['m_30'], 'location_costs_m31': loc_specific_costs['m_31'],
        'location_costs_m32': loc_specific_costs['m_32'], 'location_costs_m33': loc_specific_costs['m_33'], 'location_costs_m34': loc_specific_costs['m_33'],
        'location_costs_m34': loc_specific_costs['m_34'], 'location_costs_m35': loc_specific_costs['m_35'], 'location_costs_m36': loc_specific_costs['m_36'],
        'location_costs_yr3': 0 #loc_specific_costs['yr_3']
    })

    computation = merge_two_dicts(computation, {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'insurance_costs_m1': insurance_costs['m_01'], 'insurance_costs_m2': insurance_costs['m_02'], 'insurance_costs_m3': insurance_costs['m_03'],
        'insurance_costs_m4': insurance_costs['m_04'], 'insurance_costs_m5': insurance_costs['m_05'], 'insurance_costs_m6': insurance_costs['m_06'],
        'insurance_costs_m7': insurance_costs['m_07'], 'insurance_costs_m8': insurance_costs['m_08'], 'insurance_costs_m9': insurance_costs['m_09'],
        'insurance_costs_m10': insurance_costs['m_10'], 'insurance_costs_m11': insurance_costs['m_11'], 'insurance_costs_m12': insurance_costs['m_12'],
        'insurance_costs_yr1': insurance_costs['yr_1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'insurance_costs_m13': insurance_costs['m_13'], 'insurance_costs_m14': insurance_costs['m_14'], 'insurance_costs_m15': insurance_costs['m_15'],
        'insurance_costs_m16': insurance_costs['m_16'], 'insurance_costs_m17': insurance_costs['m_17'], 'insurance_costs_m18': insurance_costs['m_18'],
        'insurance_costs_m19': insurance_costs['m_19'], 'insurance_costs_m20': insurance_costs['m_20'], 'insurance_costs_m21': insurance_costs['m_21'],
        'insurance_costs_m22': insurance_costs['m_22'], 'insurance_costs_m23': insurance_costs['m_23'], 'insurance_costs_m24': insurance_costs['m_24'],
        'insurance_costs_yr2': insurance_costs['yr_2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'insurance_costs_m25': insurance_costs['m_25'], 'insurance_costs_m26': insurance_costs['m_26'], 'insurance_costs_m27': insurance_costs['m_27'],
        'insurance_costs_m28': insurance_costs['m_28'], 'insurance_costs_m29': insurance_costs['m_30'], 'insurance_costs_m31': insurance_costs['m_31'],
        'insurance_costs_m32': insurance_costs['m_32'], 'insurance_costs_m33': insurance_costs['m_33'], 'insurance_costs_m34': insurance_costs['m_33'],
        'insurance_costs_m34': insurance_costs['m_34'], 'insurance_costs_m35': insurance_costs['m_35'], 'insurance_costs_m36': insurance_costs['m_36'],
        'insurance_costs_yr3': 0 #insurance_costs['yr_3']
    })

    computation = merge_two_dicts(computation, {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'admin_costs_m1': admin_costs['m_01'], 'admin_costs_m2': admin_costs['m_02'], 'admin_costs_m3': admin_costs['m_03'],
        'admin_costs_m4': admin_costs['m_04'], 'admin_costs_m5': admin_costs['m_05'], 'admin_costs_m6': admin_costs['m_06'],
        'admin_costs_m7': admin_costs['m_07'], 'admin_costs_m8': admin_costs['m_08'], 'admin_costs_m9': admin_costs['m_09'],
        'admin_costs_m10': admin_costs['m_10'], 'admin_costs_m11': admin_costs['m_11'], 'admin_costs_m12': admin_costs['m_12'],
        'admin_costs_yr1': admin_costs['yr_1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'admin_costs_m13': admin_costs['m_13'], 'admin_costs_m14': admin_costs['m_14'], 'admin_costs_m15': admin_costs['m_15'],
        'admin_costs_m16': admin_costs['m_16'], 'admin_costs_m17': admin_costs['m_17'], 'admin_costs_m18': admin_costs['m_18'],
        'admin_costs_m19': admin_costs['m_19'], 'admin_costs_m20': admin_costs['m_20'], 'admin_costs_m21': admin_costs['m_21'],
        'admin_costs_m22': admin_costs['m_22'], 'admin_costs_m23': admin_costs['m_23'], 'admin_costs_m24': admin_costs['m_24'],
        'admin_costs_yr2': admin_costs['yr_2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'admin_costs_m25': admin_costs['m_25'], 'admin_costs_m26': admin_costs['m_26'], 'admin_costs_m27': admin_costs['m_27'],
        'admin_costs_m28': admin_costs['m_28'], 'admin_costs_m29': admin_costs['m_30'], 'admin_costs_m31': admin_costs['m_31'],
        'admin_costs_m32': admin_costs['m_32'], 'admin_costs_m33': admin_costs['m_33'], 'admin_costs_m34': admin_costs['m_33'],
        'admin_costs_m34': admin_costs['m_34'], 'admin_costs_m35': admin_costs['m_35'], 'admin_costs_m36': admin_costs['m_36'],
        'admin_costs_yr3': 0 #admin_costs['yr_3']
    })

    computation = merge_two_dicts(computation, {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'license_costs_m1': license_reg_costs['m_01'], 'license_costs_m2': license_reg_costs['m_02'], 'license_costs_m3': license_reg_costs['m_03'],
        'license_costs_m4': license_reg_costs['m_04'], 'license_costs_m5': license_reg_costs['m_05'], 'license_costs_m6': license_reg_costs['m_06'],
        'license_costs_m7': license_reg_costs['m_07'], 'license_costs_m8': license_reg_costs['m_08'], 'license_costs_m9': license_reg_costs['m_09'],
        'license_costs_m10': license_reg_costs['m_10'], 'license_costs_m11': license_reg_costs['m_11'], 'license_costs_m12': license_reg_costs['m_12'],
        'license_costs_yr1': license_reg_costs['yr_1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'license_costs_m13': license_reg_costs['m_13'], 'license_costs_m14': license_reg_costs['m_14'], 'license_costs_m15': license_reg_costs['m_15'],
        'license_costs_m16': license_reg_costs['m_16'], 'license_costs_m17': license_reg_costs['m_17'], 'license_costs_m18': license_reg_costs['m_18'],
        'license_costs_m19': license_reg_costs['m_19'], 'license_costs_m20': license_reg_costs['m_20'], 'license_costs_m21': license_reg_costs['m_21'],
        'license_costs_m22': license_reg_costs['m_22'], 'license_costs_m23': license_reg_costs['m_23'], 'license_costs_m24': license_reg_costs['m_24'],
        'license_costs_yr2': license_reg_costs['yr_2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'license_costs_m25': license_reg_costs['m_25'], 'license_costs_m26': license_reg_costs['m_26'], 'license_costs_m27': license_reg_costs['m_27'],
        'license_costs_m28': license_reg_costs['m_28'], 'license_costs_m29': license_reg_costs['m_30'], 'license_costs_m31': license_reg_costs['m_31'],
        'license_costs_m32': license_reg_costs['m_32'], 'license_costs_m33': license_reg_costs['m_33'], 'license_costs_m34': license_reg_costs['m_33'],
        'license_costs_m34': license_reg_costs['m_34'], 'license_costs_m35': license_reg_costs['m_35'], 'license_costs_m36': license_reg_costs['m_36'],
        'license_costs_yr3': 0 #license_reg_costs['yr_3']
    })

    computation = merge_two_dicts(computation, {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'marketing_costs_m1': marketing_costs['m_01'], 'marketing_costs_m2': marketing_costs['m_02'], 'marketing_costs_m3': marketing_costs['m_03'],
        'marketing_costs_m4': marketing_costs['m_04'], 'marketing_costs_m5': marketing_costs['m_05'], 'marketing_costs_m6': marketing_costs['m_06'],
        'marketing_costs_m7': marketing_costs['m_07'], 'marketing_costs_m8': marketing_costs['m_08'], 'marketing_costs_m9': marketing_costs['m_09'],
        'marketing_costs_m10': marketing_costs['m_10'], 'marketing_costs_m11': marketing_costs['m_11'], 'marketing_costs_m12': marketing_costs['m_12'],
        'marketing_costs_yr1': marketing_costs['yr_1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'marketing_costs_m13': marketing_costs['m_13'], 'marketing_costs_m14': marketing_costs['m_14'], 'marketing_costs_m15': marketing_costs['m_15'],
        'marketing_costs_m16': marketing_costs['m_16'], 'marketing_costs_m17': marketing_costs['m_17'], 'marketing_costs_m18': marketing_costs['m_18'],
        'marketing_costs_m19': marketing_costs['m_19'], 'marketing_costs_m20': marketing_costs['m_20'], 'marketing_costs_m21': marketing_costs['m_21'],
        'marketing_costs_m22': marketing_costs['m_22'], 'marketing_costs_m23': marketing_costs['m_23'], 'marketing_costs_m24': marketing_costs['m_24'],
        'marketing_costs_yr2': marketing_costs['yr_2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'marketing_costs_m25': marketing_costs['m_25'], 'marketing_costs_m26': marketing_costs['m_26'], 'marketing_costs_m27': marketing_costs['m_27'],
        'marketing_costs_m28': marketing_costs['m_28'], 'marketing_costs_m29': marketing_costs['m_30'], 'marketing_costs_m31': marketing_costs['m_31'],
        'marketing_costs_m32': marketing_costs['m_32'], 'marketing_costs_m33': marketing_costs['m_33'], 'marketing_costs_m34': marketing_costs['m_33'],
        'marketing_costs_m34': marketing_costs['m_34'], 'marketing_costs_m35': marketing_costs['m_35'], 'marketing_costs_m36': marketing_costs['m_36'],
        'marketing_costs_yr3': 0 #marketing_costs['yr_3']
    })

    # computation = merge_two_dicts(computation, {
    #     # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
    #     'sales_expense_m1': sales_expense['m_01'], 'sales_expense_m2': sales_expense['m_02'], 'sales_expense_m3': sales_expense['m_03'],
    #     'sales_expense_m4': sales_expense['m_04'], 'sales_expense_m5': sales_expense['m_05'], 'sales_expense_m6': sales_expense['m_06'],
    #     'sales_expense_m7': sales_expense['m_07'], 'sales_expense_m8': sales_expense['m_08'], 'sales_expense_m9': sales_expense['m_09'],
    #     'sales_expense_m10': sales_expense['m_10'], 'sales_expense_m11': sales_expense['m_11'], 'sales_expense_m12': sales_expense['m_12'],
    #     'sales_expense_yr1': sales_expense['yr_1'],
    #
    #     # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
    #     'sales_expense_m13': sales_expense['m_13'], 'sales_expense_m14': sales_expense['m_14'], 'sales_expense_m15': sales_expense['m_15'],
    #     'sales_expense_m16': sales_expense['m_16'], 'sales_expense_m17': sales_expense['m_17'], 'sales_expense_m18': sales_expense['m_18'],
    #     'sales_expense_m19': sales_expense['m_19'], 'sales_expense_m20': sales_expense['m_20'], 'sales_expense_m21': sales_expense['m_21'],
    #     'sales_expense_m22': sales_expense['m_22'], 'sales_expense_m23': sales_expense['m_23'], 'sales_expense_m24': sales_expense['m_24'],
    #     'sales_expense_yr2': sales_expense['yr_2'],
    #
    #     # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
    #     'sales_expense_m25': sales_expense['m_25'], 'sales_expense_m26': sales_expense['m_26'], 'sales_expense_m27': sales_expense['m_27'],
    #     'sales_expense_m28': sales_expense['m_28'], 'sales_expense_m29': sales_expense['m_30'], 'sales_expense_m31': sales_expense['m_31'],
    #     'sales_expense_m32': sales_expense['m_32'], 'sales_expense_m33': sales_expense['m_33'], 'sales_expense_m34': sales_expense['m_33'],
    #     'sales_expense_m34': sales_expense['m_34'], 'sales_expense_m35': sales_expense['m_35'], 'sales_expense_m36': sales_expense['m_36'],
    #     'sales_expense_yr3': 0 #sales_expense['yr_3']
    # })

    computation = merge_two_dicts(computation, {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'bank_fees_m1': banking_costs['m_01'], 'bank_fees_m2': banking_costs['m_02'], 'bank_fees_m3': banking_costs['m_03'],
        'bank_fees_m4': banking_costs['m_04'], 'bank_fees_m5': banking_costs['m_05'], 'bank_fees_m6': banking_costs['m_06'],
        'bank_fees_m7': banking_costs['m_07'], 'bank_fees_m8': banking_costs['m_08'], 'bank_fees_m9': banking_costs['m_09'],
        'bank_fees_m10': banking_costs['m_10'], 'bank_fees_m11': banking_costs['m_11'], 'bank_fees_m12': banking_costs['m_12'],
        'bank_fees_yr1': banking_costs['yr_1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'bank_fees_m13': banking_costs['m_13'], 'bank_fees_m14': banking_costs['m_14'], 'bank_fees_m15': banking_costs['m_15'],
        'bank_fees_m16': banking_costs['m_16'], 'bank_fees_m17': banking_costs['m_17'], 'bank_fees_m18': banking_costs['m_18'],
        'bank_fees_m19': banking_costs['m_19'], 'bank_fees_m20': banking_costs['m_20'], 'bank_fees_m21': banking_costs['m_21'],
        'bank_fees_m22': banking_costs['m_22'], 'bank_fees_m23': banking_costs['m_23'], 'bank_fees_m24': banking_costs['m_24'],
        'bank_fees_yr2': banking_costs['yr_2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'bank_fees_m25': banking_costs['m_25'], 'bank_fees_m26': banking_costs['m_26'], 'bank_fees_m27': banking_costs['m_27'],
        'bank_fees_m28': banking_costs['m_28'], 'bank_fees_m29': banking_costs['m_30'], 'bank_fees_m31': banking_costs['m_31'],
        'bank_fees_m32': banking_costs['m_32'], 'bank_fees_m33': banking_costs['m_33'], 'bank_fees_m34': banking_costs['m_33'],
        'bank_fees_m34': banking_costs['m_34'], 'bank_fees_m35': banking_costs['m_35'], 'bank_fees_m36': banking_costs['m_36'],
        'bank_fees_yr3': 0 #banking_costs['yr_3']
    })

    # computation = merge_two_dicts(computation, {
    #     # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
    #     'bank_fees_m1': salaries['m_01'], 'bank_fees_m2': salaries['m_02'], 'bank_fees_m3': salaries['m_03'],
    #     'bank_fees_m4': salaries['m_04'], 'bank_fees_m5': salaries['m_05'], 'bank_fees_m6': salaries['m_06'],
    #     'bank_fees_m7': salaries['m_07'], 'bank_fees_m8': salaries['m_08'], 'bank_fees_m9': salaries['m_09'],
    #     'bank_fees_m10': salaries['m_10'], 'bank_fees_m11': salaries['m_11'], 'bank_fees_m12': salaries['m_12'],
    #     'bank_fees_yr1': salaries['yr_1'],
    #
    #     # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
    #     'bank_fees_m13': salaries['m_13'], 'bank_fees_m14': salaries['m_14'], 'bank_fees_m15': salaries['m_15'],
    #     'bank_fees_m16': salaries['m_16'], 'bank_fees_m17': salaries['m_17'], 'bank_fees_m18': salaries['m_18'],
    #     'bank_fees_m19': salaries['m_19'], 'bank_fees_m20': salaries['m_20'], 'bank_fees_m21': salaries['m_21'],
    #     'bank_fees_m22': salaries['m_22'], 'bank_fees_m23': salaries['m_23'], 'bank_fees_m24': salaries['m_24'],
    #     'bank_fees_yr2': salaries['yr_2'],
    #
    #     # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
    #     'bank_fees_m25': salaries['m_25'], 'bank_fees_m26': salaries['m_26'], 'bank_fees_m27': salaries['m_27'],
    #     'bank_fees_m28': salaries['m_28'], 'bank_fees_m29': salaries['m_30'], 'bank_fees_m31': salaries['m_31'],
    #     'bank_fees_m32': salaries['m_32'], 'bank_fees_m33': salaries['m_33'], 'bank_fees_m34': salaries['m_33'],
    #     'bank_fees_m34': salaries['m_34'], 'bank_fees_m35': salaries['m_35'], 'bank_fees_m36': salaries['m_36'],
    #     'bank_fees_yr3': 0 #salaries['yr_3']
    # })

    computation = merge_two_dicts(computation, {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'comm_costs_m1': communication_costs['m_01'], 'comm_costs_m2': communication_costs['m_02'], 'comm_costs_m3': communication_costs['m_03'],
        'comm_costs_m4': communication_costs['m_04'], 'comm_costs_m5': communication_costs['m_05'], 'comm_costs_m6': communication_costs['m_06'],
        'comm_costs_m7': communication_costs['m_07'], 'comm_costs_m8': communication_costs['m_08'], 'comm_costs_m9': communication_costs['m_09'],
        'comm_costs_m10': communication_costs['m_10'], 'comm_costs_m11': communication_costs['m_11'], 'comm_costs_m12': communication_costs['m_12'],
        'comm_costs_yr1': communication_costs['yr_1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'comm_costs_m13': communication_costs['m_13'], 'comm_costs_m14': communication_costs['m_14'], 'comm_costs_m15': communication_costs['m_15'],
        'comm_costs_m16': communication_costs['m_16'], 'comm_costs_m17': communication_costs['m_17'], 'comm_costs_m18': communication_costs['m_18'],
        'comm_costs_m19': communication_costs['m_19'], 'comm_costs_m20': communication_costs['m_20'], 'comm_costs_m21': communication_costs['m_21'],
        'comm_costs_m22': communication_costs['m_22'], 'comm_costs_m23': communication_costs['m_23'], 'comm_costs_m24': communication_costs['m_24'],
        'comm_costs_yr2': communication_costs['yr_2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'comm_costs_m25': communication_costs['m_25'], 'comm_costs_m26': communication_costs['m_26'], 'comm_costs_m27': communication_costs['m_27'],
        'comm_costs_m28': communication_costs['m_28'], 'comm_costs_m29': communication_costs['m_30'], 'comm_costs_m31': communication_costs['m_31'],
        'comm_costs_m32': communication_costs['m_32'], 'comm_costs_m33': communication_costs['m_33'], 'comm_costs_m34': communication_costs['m_33'],
        'comm_costs_m34': communication_costs['m_34'], 'comm_costs_m35': communication_costs['m_35'], 'comm_costs_m36': communication_costs['m_36'],
        'comm_costs_yr3': 0 #communication_costs['yr_3']
    })

    computation = merge_two_dicts(computation, {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'transportation_costs_m1': transportation_costs['m_01'], 'transportation_costs_m2': transportation_costs['m_02'], 'transportation_costs_m3': transportation_costs['m_03'],
        'transportation_costs_m4': transportation_costs['m_04'], 'transportation_costs_m5': transportation_costs['m_05'], 'transportation_costs_m6': transportation_costs['m_06'],
        'transportation_costs_m7': transportation_costs['m_07'], 'transportation_costs_m8': transportation_costs['m_08'], 'transportation_costs_m9': transportation_costs['m_09'],
        'transportation_costs_m10': transportation_costs['m_10'], 'transportation_costs_m11': transportation_costs['m_11'], 'transportation_costs_m12': transportation_costs['m_12'],
        'transportation_costs_yr1': transportation_costs['yr_1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'transportation_costs_m13': transportation_costs['m_13'], 'transportation_costs_m14': transportation_costs['m_14'], 'transportation_costs_m15': transportation_costs['m_15'],
        'transportation_costs_m16': transportation_costs['m_16'], 'transportation_costs_m17': transportation_costs['m_17'], 'transportation_costs_m18': transportation_costs['m_18'],
        'transportation_costs_m19': transportation_costs['m_19'], 'transportation_costs_m20': transportation_costs['m_20'], 'transportation_costs_m21': transportation_costs['m_21'],
        'transportation_costs_m22': transportation_costs['m_22'], 'transportation_costs_m23': transportation_costs['m_23'], 'transportation_costs_m24': transportation_costs['m_24'],
        'transportation_costs_yr2': transportation_costs['yr_2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'transportation_costs_m25': transportation_costs['m_25'], 'transportation_costs_m26': transportation_costs['m_26'], 'transportation_costs_m27': transportation_costs['m_27'],
        'transportation_costs_m28': transportation_costs['m_28'], 'transportation_costs_m29': transportation_costs['m_30'], 'transportation_costs_m31': transportation_costs['m_31'],
        'transportation_costs_m32': transportation_costs['m_32'], 'transportation_costs_m33': transportation_costs['m_33'], 'transportation_costs_m34': transportation_costs['m_33'],
        'transportation_costs_m34': transportation_costs['m_34'], 'transportation_costs_m35': transportation_costs['m_35'], 'transportation_costs_m36': transportation_costs['m_36'],
        'transportation_costs_yr3': 0 #transportation_costs['yr_3']
    })

    # computation = merge_two_dicts(computation, {
    #     # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
    #     'sub_costs_m1': sub_costs['m_01'], 'sub_costs_m2': sub_costs['m_02'], 'sub_costs_m3': sub_costs['m_03'],
    #     'sub_costs_m4': sub_costs['m_04'], 'sub_costs_m5': sub_costs['m_05'], 'sub_costs_m6': sub_costs['m_06'],
    #     'sub_costs_m7': sub_costs['m_07'], 'sub_costs_m8': sub_costs['m_08'], 'sub_costs_m9': sub_costs['m_09'],
    #     'sub_costs_m10': sub_costs['m_10'], 'sub_costs_m11': sub_costs['m_11'], 'sub_costs_m12': sub_costs['m_12'],
    #     'sub_costs_yr1': sub_costs['yr_1'],
    #
    #     # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
    #     'sub_costs_m13': sub_costs['m_13'], 'sub_costs_m14': sub_costs['m_14'], 'sub_costs_m15': sub_costs['m_15'],
    #     'sub_costs_m16': sub_costs['m_16'], 'sub_costs_m17': sub_costs['m_17'], 'sub_costs_m18': sub_costs['m_18'],
    #     'sub_costs_m19': sub_costs['m_19'], 'sub_costs_m20': sub_costs['m_20'], 'sub_costs_m21': sub_costs['m_21'],
    #     'sub_costs_m22': sub_costs['m_22'], 'sub_costs_m23': sub_costs['m_23'], 'sub_costs_m24': sub_costs['m_24'],
    #     'sub_costs_yr2': sub_costs['yr_2'],
    #
    #     # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
    #     'sub_costs_m25': sub_costs['m_25'], 'sub_costs_m26': sub_costs['m_26'], 'sub_costs_m27': sub_costs['m_27'],
    #     'sub_costs_m28': sub_costs['m_28'], 'sub_costs_m29': sub_costs['m_30'], 'sub_costs_m31': sub_costs['m_31'],
    #     'sub_costs_m32': sub_costs['m_32'], 'sub_costs_m33': sub_costs['m_33'], 'sub_costs_m34': sub_costs['m_33'],
    #     'sub_costs_m34': sub_costs['m_34'], 'sub_costs_m35': sub_costs['m_35'], 'sub_costs_m36': sub_costs['m_36'],
    #     'sub_costs_yr3': 0 #sub_costs['yr_3']
    # })

    computation = merge_two_dicts(computation, {
        # - - - - - - - - - - - - - - # YEAR 1 # - - - - - - - - - - - - - - #
        'lease_costs_m1': equipment_lease['m_01'], 'lease_costs_m2': equipment_lease['m_02'], 'lease_costs_m3': equipment_lease['m_03'],
        'lease_costs_m4': equipment_lease['m_04'], 'lease_costs_m5': equipment_lease['m_05'], 'lease_costs_m6': equipment_lease['m_06'],
        'lease_costs_m7': equipment_lease['m_07'], 'lease_costs_m8': equipment_lease['m_08'], 'lease_costs_m9': equipment_lease['m_09'],
        'lease_costs_m10': equipment_lease['m_10'], 'lease_costs_m11': equipment_lease['m_11'], 'lease_costs_m12': equipment_lease['m_12'],
        'lease_costs_yr1': equipment_lease['yr_1'],

        # - - - - - - - - - - - - - - # YEAR 2 # - - - - - - - - - - - - - - #
        'lease_costs_m13': equipment_lease['m_13'], 'lease_costs_m14': equipment_lease['m_14'], 'lease_costs_m15': equipment_lease['m_15'],
        'lease_costs_m16': equipment_lease['m_16'], 'lease_costs_m17': equipment_lease['m_17'], 'lease_costs_m18': equipment_lease['m_18'],
        'lease_costs_m19': equipment_lease['m_19'], 'lease_costs_m20': equipment_lease['m_20'], 'lease_costs_m21': equipment_lease['m_21'],
        'lease_costs_m22': equipment_lease['m_22'], 'lease_costs_m23': equipment_lease['m_23'], 'lease_costs_m24': equipment_lease['m_24'],
        'lease_costs_yr2': equipment_lease['yr_2'],

        # - - - - - - - - - - - - - - # YEAR 3 # - - - - - - - - - - - - - - #
        'lease_costs_m25': equipment_lease['m_25'], 'lease_costs_m26': equipment_lease['m_26'], 'lease_costs_m27': equipment_lease['m_27'],
        'lease_costs_m28': equipment_lease['m_28'], 'lease_costs_m29': equipment_lease['m_30'], 'lease_costs_m31': equipment_lease['m_31'],
        'lease_costs_m32': equipment_lease['m_32'], 'lease_costs_m33': equipment_lease['m_33'], 'lease_costs_m34': equipment_lease['m_33'],
        'lease_costs_m34': equipment_lease['m_34'], 'lease_costs_m35': equipment_lease['m_35'], 'lease_costs_m36': equipment_lease['m_36'],
        'lease_costs_yr3': 0 #equipment_lease['yr_3']
    })




    #=============#
    # SAVING DATA #
    #=============#
    answer.content = computation
    answer.save()

    # Return result.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
    }
