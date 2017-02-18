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


def get_answer_content(workspace, qid):
    q = QuestionAnswer.objects.get(
        question_id=qid,
        workspace=workspace
    )
    return q.content


def get_long_term_assets(q4):
    total_yr1 = 0.0
    total_yr2 = 0.0
    total_yr3 = 0.0
    for item in q4:
        if item['var_3'] == "Long-term asset":
            total_yr1 += float(item['var_5'])
            total_yr2 += float(item['var_6'])
            total_yr3 += float(item['var_7'])
    return {
        'yr1': total_yr1,
        'yr2': total_yr2,
        'yr3': total_yr3
    }


def get_assets_to_purchase(q1):
    total_yr1 = 0.0
    total_yr2 = 0.0
    total_yr3 = 0.0
    for item in q1:
        total_yr1 += float(item['var_5'])
        total_yr2 += float(item['var_6'])
        total_yr3 += float(item['var_7'])
    return {
        'yr1': total_yr1,
        'yr2': total_yr2,
        'yr3': total_yr3
    }


def get_inventory(q2, q5):
    total = 0.00
    index = q5['var_1']

    if index >= 1:
        total += q2['materials_month_1']

    if index >= 2:
        total += q2['materials_month_2']

    if index >= 3:
        total += q2['materials_month_3']

    if index >= 4:
        total += q2['materials_month_4']

    if index >= 5:
        total += q2['materials_month_5']

    if index >= 6:
        total += q2['materials_month_6']

    if index >= 7:
        total += q2['materials_month_7']

    if index >= 8:
        total += q2['materials_month_8']

    if index >= 9:
        total += q2['materials_month_9']

    if index >= 10:
        total += q2['materials_month_10']

    if index >= 11:
        total += q2['materials_month_11']

    if index >= 12:
        total += q2['materials_month_12']

    return total


def get_salary(q3):
    # Convert
    value_str = q3['var_1_other'] if q3['var_1_other'] else q3['var_1']
    value_str = value_str.replace('$', '')
    value_str = value_str.replace(',', '')
    value = float(value_str)

    # Compute.
    ent_cash_startup_req = value * 12.00

    # Return.
    return ent_cash_startup_req


def get_short_term_assets(answer_content):
    print(answer_content)
    total_yr1 = 0.0
    total_yr2 = 0.0
    total_yr3 = 0.0
    for item in answer_content:
        if item['var_3'] == "Short-term asset":
            total_yr1 += float(item['var_5'])
            total_yr2 += float(item['var_6'])
            total_yr3 += float(item['var_7'])
    return {
        'yr1': total_yr1,
        'yr2': total_yr2,
        'yr3': total_yr3
    }

def get_short_term_liabilities(answer_content):
    total_yr1 = 0.0
    total_yr2 = 0.0
    total_yr3 = 0.0
    for item in answer_content:
        if item['var_3'] == "Short-term liability":
            total_yr1 += float(item['var_5'])
            total_yr2 += float(item['var_6'])
            total_yr3 += float(item['var_7'])
    return {
        'yr1': total_yr1,
        'yr2': total_yr2,
        'yr3': total_yr3
    }


def get_long_term_liabilities(answer_content):
    total_yr1 = 0.0
    total_yr2 = 0.0
    total_yr3 = 0.0
    for item in answer_content:
        if item['var_3'] == "Long-term liability":
            total_yr1 += float(item['var_5'])
            total_yr2 += float(item['var_6'])
            total_yr3 += float(item['var_7'])
    return {
        'yr1': total_yr1,
        'yr2': total_yr2,
        'yr3': total_yr3
    }


@register.inclusion_tag('templatetags/question/template_066.html')
def render_question_type_066(workspace, module, node, question, answer):
    #====================#
    # FETCH DEPENDENCIES #
    #====================#
    q1_qid = int_or_none(question.dependency['q1_qid']) # "q1_qid": 139,
    q2_qid = int_or_none(question.dependency['q2_qid']) # "q2_qid": 101,
    q3_qid = int_or_none(question.dependency['q3_qid']) # "q3_qid": 146,
    q4_qid = int_or_none(question.dependency['q4_qid']) # "q4_qid": 140,
    q5_qid = int_or_none(question.dependency['q5_qid']) # "q4_qid": 141

    #===============#
    # FETCH ANSWERS #
    #===============#
    q1 = get_answer_content(workspace, q1_qid)
    q2 = get_answer_content(workspace, q2_qid)
    q3 = get_answer_content(workspace, q3_qid)
    q4 = get_answer_content(workspace, q4_qid)
    q5 = get_answer_content(workspace, q5_qid)

    #==============#
    # COMPUTATIONS #
    #==============#
    total_yr1 = 0.0
    total_yr2 = 0.0
    total_yr3 = 0.0

    # Start-up Costs
    #------------------------
    long_term_assets = get_long_term_assets(q4) # Assets Owned.

    # Cash Required
    #------------------------
    # Assets to Purchase
    equipment_costs = get_assets_to_purchase(q1)

    # Inventory
    startup_inventory_req = get_inventory(q2, q5)

    # Salary
    ent_cash_startup_req = get_salary(q3)

    # Total Start-up Costs
    cash_required = startup_inventory_req + ent_cash_startup_req + equipment_costs['yr1']

    # Funds Available
    short_term_assets = get_short_term_assets(q4)
    short_term_liabilities = get_short_term_liabilities(q4)
    long_term_liabilities = get_long_term_liabilities(q4)

    # Total Funds Available
    funds_available = short_term_assets['yr1'] + short_term_liabilities['yr1'] + long_term_liabilities['yr1']

    # Start-up Deficit/Surplus
    net_startup_deficit_surplus = cash_required - funds_available

    #=============#
    # SAVING DATA #
    #=============#
    answer.content = {
        'asset_y1_costs_total': long_term_assets['yr1'],
        'equipment_y1_costs': equipment_costs['yr1'],
        'startup_inventory_req': startup_inventory_req,
        'ent_cash_startup_req': ent_cash_startup_req,
        'cash_required': cash_required,
        'short_term_assets_y1': short_term_assets['yr1'],
        'short_term_liabilities_y1': short_term_liabilities['yr1'],
        'long_term_liabilities_y1': long_term_liabilities['yr1'],
        'funds_available': funds_available,
        'net_startup_deficit_surplus': net_startup_deficit_surplus
    }
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
