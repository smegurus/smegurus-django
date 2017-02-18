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


@register.inclusion_tag('templatetags/question/template_067.html')
def render_question_type_067(workspace, module, node, question, answer):
    #================================#
    # Fetch & pre-process questions. #
    #================================#

    # PK 104 - Stage 7, Marketing Costs
    q1_qid = int_or_none(question.dependency['q1_qid'])
    marketing_costs = get_table_for_qid(workspace, q1_qid)

    # PK 108 - Salaries
    q2_qid = int_or_none(question.dependency['q2_qid'])
    q2 = QuestionAnswer.objects.get(
        question_id=q2_qid,
        workspace=workspace
    )
    q2 = q2.content

    # PK107 - Pro Fees
    q3_qid = int_or_none(question.dependency['q3_qid'])
    pro_fees = get_table_for_qid(workspace, q3_qid)

    # PK112 - Admin. costs
    q4_qid = int_or_none(question.dependency['q4_qid'])
    admin_costs = get_table_for_qid(workspace, q4_qid)

    # PK125 - Sales expenses
    q5_qid = int_or_none(question.dependency['q5_qid'])
    sales_expenses = get_table_for_qid(workspace, q5_qid)

    # PK110 - Location specific costs
    q6_qid = int_or_none(question.dependency['q6_qid'])
    loc_specific_costs = get_table_for_qid(workspace, q6_qid)

    # PK115 - Insurance costs
    q7_qid = int_or_none(question.dependency['q7_qid'])
    insurance_costs = get_table_for_qid(workspace, q7_qid)

    # PK113 - License/Registration costs
    q8_qid = int_or_none(question.dependency['q8_qid'])
    license_reg_costs = get_table_for_qid(workspace, q8_qid)

    # PK109 - Transportation costs
    q9_qid = int_or_none(question.dependency['q9_qid'])
    transportation_costs = get_table_for_qid(workspace, q9_qid)

    # PK117 - Banking costs
    q10_qid = int_or_none(question.dependency['q10_qid'])
    banking_costs = get_table_for_qid(workspace, q10_qid)

    # PK119 - Office supplies
    q11_qid = int_or_none(question.dependency['q11_qid'])
    office_supplies_cost = get_table_for_qid(workspace, q11_qid)

    # PK121 - Communication Costs
    q12_qid = int_or_none(question.dependency['q12_qid'])
    communication_costs = get_table_for_qid(workspace, q12_qid)

    # PK127 - Membership fees
    q13_qid = int_or_none(question.dependency['q13_qid'])
    membership_fees = get_table_for_qid(workspace, q13_qid)

    # PK129 - Equipment lease
    q14_qid = int_or_none(question.dependency['q14_qid'])
    equipment_lease = get_table_for_qid(workspace, q14_qid)

    # PK131 - Maintenance
    q15_qid = int_or_none(question.dependency['q15_qid'])
    equipment_lease = get_table_for_qid(workspace, q15_qid)

    # PK133 - Other
    q16_qid = int_or_none(question.dependency['q16_qid'])
    other_costs = get_table_for_qid(workspace, q16_qid)

    # PK135 - Misc
    q17_qid = int_or_none(question.dependency['q17_qid'])
    misc_costs = get_table_for_qid(workspace, q17_qid)

    #================================#
    # Process question computations. #
    #================================#
    computation = {} # Variable to store our table.

    # Start-Up Surplus/Deficit
    #TODO

    # General & Admin Expenses
    #TODO

    # Total G & A Expenses
    #TODO: Imp.

    # Return result.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        # 'picked': answer.content,
    }
