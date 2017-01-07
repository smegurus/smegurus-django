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


register = template.Library()


def scalar_multiply_by(arr, value):
    arr['yr1'] *= value
    arr['yr2'] *= value
    arr['yr3'] *= value
    arr['total'] *= value
    return arr


def matrix_subtract_by(arr1, arr2):
    arr1['yr1'] -= arr2['yr1']
    arr1['yr2'] -= arr2['yr2']
    arr1['yr3'] -= arr2['yr3']
    arr1['total'] -= arr2['total']
    return arr1


def calculate_revenue(forcast, units_sold):
    # Caclulate the revenue per year
    revenue = {
        'yr1': forcast['sales_per_unit_yr1'] * units_sold['yr1_total'],
        'yr2': forcast['sales_per_unit_yr2'] * units_sold['yr2_total'],
        'yr3': forcast['sales_per_unit_yr3'] * units_sold['yr3_total'],
    }

    # Calculate the total revenue for three years.
    revenue['total'] = revenue['yr1'] + revenue['yr2'] + revenue['yr3']

    return revenue  # Return our computation.


def calculate_cogs(forcast, units_sold):
    # Caclulate the revenue per year
    cogs = {
        'yr1': forcast['total_cogs_yr1'] * units_sold['yr1_total'],
        'yr2': forcast['total_cogs_yr2'] * units_sold['yr2_total'],
        'yr3': forcast['total_cogs_yr3'] * units_sold['yr3_total'],
    }

    # Calculate the total revenue for three years.
    cogs['total'] = cogs['yr1'] + cogs['yr2'] + cogs['yr3']

    return cogs  # Return our computation.


def calculate_labour(forcast, units_sold):
    # Caclulate the revenue per year
    labour = {
        'yr1': forcast['labour_yr1'] * units_sold['yr1_total'],
        'yr2': forcast['labour_yr2'] * units_sold['yr2_total'],
        'yr3': forcast['labour_yr3'] * units_sold['yr3_total'],
    }

    # Calculate the total revenue for three years.
    labour['total'] = labour['yr1'] + labour['yr2'] + labour['yr3']

    return labour  # Return our computation.


def calculate_materials(forcast, units_sold):
    materials = {
        'yr1': forcast['materials_yr1'] * units_sold['yr1_total'],
        'yr2': forcast['materials_yr2'] * units_sold['yr2_total'],
        'yr3': forcast['materials_yr3'] * units_sold['yr3_total'],
    }
    materials['total'] = materials['yr1'] + materials['yr2'] + materials['yr3']
    return materials


def calculate_overhead(forcast, units_sold):
    overhead = {
        'yr1': forcast['overhead_yr1'] * units_sold['yr1_total'],
        'yr2': forcast['overhead_yr2'] * units_sold['yr2_total'],
        'yr3': forcast['overhead_yr3'] * units_sold['yr3_total'],
    }
    overhead['total'] = overhead['yr1'] + overhead['yr2'] + overhead['yr3']
    return overhead


@register.inclusion_tag('templatetags/question/template_057.html')
def render_question_type_057(workspace, module, node, question, answer):
    """
    ============================================================================
    Dependency:
    ============================================================================
    - QID: 100 | 01 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/4/
    - QID: 99  | 02 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/3/
    - QID: 77  | 03 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/4/17/
    - QID: 78  | 04 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/4/18/
    - QID: 79  | 05 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/4/19/
    - QID: 80  | 06 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/4/20/
    - QID: 142 | 07 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/4/21/
    - QID: 143 | 08 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/4/22/
    - QID: 85  | 09 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/5/5/
    - QID: 86  | 10 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/5/6/
    - QID: 90  | 11 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/5/10/
    - QID: 105 | 12 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/9/
    - QID: 108 | 13 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/12/
    - QID: 111 | 14 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/15/
    - QID: 114 | 15 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/18/
    - QID: 116 | 16 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/20/
    - QID: 120 | 17 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/24/
    - QID: 122 | 18 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/26/
    - QID: 124 | 19 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/28/
    - QID: 126 | 20 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/30/
    - QID: 128 | 21 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/32/
    - QID: 130 | 22 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/34/
    - QID: 132 | 23 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/36/
    - QID: 134 | 24 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/38/
    """
    # This variable is used to keep track of the auto-generated values for the
    # three choices in this question.
    autogen = {}

    #===================#
    # CALCULATE REVENUE #
    #===================#

    # Fetch Q1
    q1_qid = int_or_none(question.dependency['q1_qid'])
    q1 = QuestionAnswer.objects.get(
        question_id=q1_qid,
        workspace=workspace
    )
    q1_picked = q1.content

    # Fetch Q2
    q2_qid = int_or_none(question.dependency['q2_qid'])
    q2 = QuestionAnswer.objects.get(
        question_id=q2_qid,
        workspace=workspace
    )
    q2_picked = q2.content

    # # Debugging Purposes only.
    # print(q1_picked)
    # print(q2_picked)
    # print("\n")

    # Calculate the revenue.
    revenue = calculate_revenue(q1_picked, q2_picked)
    # print(revenue)
    # print("\n")

    # Calculate the COGS.
    cogs = calculate_cogs(q1_picked, q2_picked)
    # print(cogs)
    # print("\n")

    # Calculate labour costs.
    labour = calculate_labour(q1_picked, q2_picked)
    # print(labour)
    # print("\n")

    # Calculate the materials cost.
    materials = calculate_materials(q1_picked, q2_picked)
    # print(materials)
    # print("\n")

    # Calculate the overhead cost.
    overhead = calculate_overhead(q1_picked, q2_picked)
    # print(overhead)
    # print("\n")

    #===================================#
    # CALCULATE SUM OF GENERAL EXPENSES #
    #===================================#

    costs = {
        "yr1": 0,
        "yr2": 0,
        "yr3": 0,
        "total": 0
    }

    # Q3 - FETCH
    q3_qid = int_or_none(question.dependency['q3_qid'])
    q3 = QuestionAnswer.objects.get(
        question_id=q3_qid,
        workspace=workspace
    )
    q3_picked = q3.content

    # Q3 - CALCULATE SUM
    for item in q3_picked:
        costs['yr1'] += float(item['var_6'])
        costs['yr2'] += float(item['var_7'])
        costs['yr3'] += float(item['var_8'])
        costs['total'] += float(item['var_6']) + float(item['var_7']) + float(item['var_8'])

    # Q4 - FETCH
    q4_qid = int_or_none(question.dependency['q4_qid'])
    q4 = QuestionAnswer.objects.get(
        question_id=q4_qid,
        workspace=workspace
    )
    q4_picked = q4.content

    # Q4 - CALCULATE SUM
    for item in q4_picked:
        costs['yr1'] += float(item['var_6'])
        costs['yr2'] += float(item['var_7'])
        costs['yr3'] += float(item['var_8'])
        costs['total'] += float(item['var_6']) + float(item['var_7']) + float(item['var_8'])

    # Q5 - FETCH
    q5_qid = int_or_none(question.dependency['q5_qid'])
    q5 = QuestionAnswer.objects.get(
        question_id=q5_qid,
        workspace=workspace
    )
    q5_picked = q5.content

    # Q5 - CALCULATE SUM
    for item in q5_picked:
        costs['yr1'] += float(item['var_6'])
        costs['yr2'] += float(item['var_7'])
        costs['yr3'] += float(item['var_8'])
        costs['total'] += float(item['var_6']) + float(item['var_7']) + float(item['var_8'])

    # Q6 - FETCH
    q6_qid = int_or_none(question.dependency['q6_qid'])
    q6 = QuestionAnswer.objects.get(
        question_id=q6_qid,
        workspace=workspace
    )
    q6_picked = q6.content

    # Q6 - CALCULATE SUM
    for item in q6_picked:
        costs['yr1'] += float(item['var_7'])
        costs['yr2'] += float(item['var_8'])
        costs['yr3'] += float(item['var_9'])
        costs['total'] += float(item['var_7']) + float(item['var_8']) + float(item['var_9'])

    # Q7 - FETCH
    q7_qid = int_or_none(question.dependency['q7_qid'])
    q7 = QuestionAnswer.objects.get(
        question_id=q4_qid,
        workspace=workspace
    )
    q7_picked = q7.content

    # Q7 - CALCULATE SUM
    for item in q7_picked:
        costs['yr1'] += float(item['var_6'])
        costs['yr2'] += float(item['var_7'])
        costs['yr3'] += float(item['var_8'])
        costs['total'] += float(item['var_6']) + float(item['var_7']) + float(item['var_8'])

    # Q8 - FETCH
    q8_qid = int_or_none(question.dependency['q8_qid'])
    q8 = QuestionAnswer.objects.get(
        question_id=q8_qid,
        workspace=workspace
    )
    q8_picked = q8.content

    # Q8 - CALCULATE SUM
    for item in q8_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q9 - FETCH
    q9_qid = int_or_none(question.dependency['q9_qid'])
    q9 = QuestionAnswer.objects.get(
        question_id=q9_qid,
        workspace=workspace
    )
    q9_picked = q9.content

    # Q9 - CALCULATE SUM
    for item in q9_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q10 - FETCH
    q10_qid = int_or_none(question.dependency['q10_qid'])
    q10 = QuestionAnswer.objects.get(
        question_id=q10_qid,
        workspace=workspace
    )
    q10_picked = q10.content

    # Q10 - CALCULATE SUM
    for item in q10_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q11 - FETCH
    q11_qid = int_or_none(question.dependency['q11_qid'])
    q11 = QuestionAnswer.objects.get(
        question_id=q11_qid,
        workspace=workspace
    )
    q11_picked = q11.content

    # Q11 - CALCULATE SUM
    for item in q11_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q12 - FETCH
    q12_qid = int_or_none(question.dependency['q12_qid'])
    q12 = QuestionAnswer.objects.get(
        question_id=q12_qid,
        workspace=workspace
    )
    q12_picked = q12.content

    # Q12 - CALCULATE SUM
    for item in q4_picked:
        costs['yr1'] += float(item['var_6'])
        costs['yr2'] += float(item['var_7'])
        costs['yr3'] += float(item['var_8'])
        costs['total'] += float(item['var_6']) + float(item['var_7']) + float(item['var_8'])

    # Q13 - FETCH
    q13_qid = int_or_none(question.dependency['q13_qid'])
    q13 = QuestionAnswer.objects.get(
        question_id=q13_qid,
        workspace=workspace
    )
    q13_picked = q13.content

    # Q13 - CALCULATE SUM
    for item in q13_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q14 - FETCH
    q14_qid = int_or_none(question.dependency['q14_qid'])
    q14 = QuestionAnswer.objects.get(
        question_id=q14_qid,
        workspace=workspace
    )
    q14_picked = q14.content

    # Q14 - CALCULATE SUM
    for item in q14_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q15 - FETCH
    q15_qid = int_or_none(question.dependency['q15_qid'])
    q15 = QuestionAnswer.objects.get(
        question_id=q15_qid,
        workspace=workspace
    )
    q15_picked = q15.content

    # Q15 - CALCULATE SUM
    for item in q15_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q16 - FETCH
    q16_qid = int_or_none(question.dependency['q16_qid'])
    q16 = QuestionAnswer.objects.get(
        question_id=q16_qid,
        workspace=workspace
    )
    q16_picked = q16.content

    # Q16 - CALCULATE SUM
    for item in q16_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q17 - FETCH
    q17_qid = int_or_none(question.dependency['q17_qid'])
    q17 = QuestionAnswer.objects.get(
        question_id=q17_qid,
        workspace=workspace
    )
    q17_picked = q17.content

    # Q17 - CALCULATE SUM
    for item in q17_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q18 - FETCH
    q18_qid = int_or_none(question.dependency['q18_qid'])
    q18 = QuestionAnswer.objects.get(
        question_id=q18_qid,
        workspace=workspace
    )
    q18_picked = q18.content

    # Q18 - CALCULATE SUM
    for item in q18_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q19 - FETCH
    q19_qid = int_or_none(question.dependency['q19_qid'])
    q19 = QuestionAnswer.objects.get(
        question_id=q19_qid,
        workspace=workspace
    )
    q19_picked = q19.content

    # Q19 - CALCULATE SUM
    for item in q19_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q20 - FETCH
    q20_qid = int_or_none(question.dependency['q20_qid'])
    q20 = QuestionAnswer.objects.get(
        question_id=q20_qid,
        workspace=workspace
    )
    q20_picked = q20.content

    # Q20 - CALCULATE SUM
    for item in q20_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q21 - FETCH
    q21_qid = int_or_none(question.dependency['q21_qid'])
    q21 = QuestionAnswer.objects.get(
        question_id=q21_qid,
        workspace=workspace
    )
    q21_picked = q21.content

    # Q21 - CALCULATE SUM
    for item in q21_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q22 - FETCH
    q22_qid = int_or_none(question.dependency['q22_qid'])
    q22 = QuestionAnswer.objects.get(
        question_id=q22_qid,
        workspace=workspace
    )
    q22_picked = q22.content

    # Q22 - CALCULATE SUM
    for item in q22_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Q23 - FETCH
    q23_qid = int_or_none(question.dependency['q23_qid'])
    q23 = QuestionAnswer.objects.get(
        question_id=q23_qid,
        workspace=workspace
    )
    q23_picked = q23.content

    # Q23 - CALCULATE SUM
    for item in q23_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])


    # Q24 - FETCH
    q24_qid = int_or_none(question.dependency['q24_qid'])
    q24 = QuestionAnswer.objects.get(
        question_id=q24_qid,
        workspace=workspace
    )
    q24_picked = q24.content

    # Q24 - CALCULATE SUM
    for item in q24_picked:
        costs['yr1'] += float(item['var_5'])
        costs['yr2'] += float(item['var_6'])
        costs['yr3'] += float(item['var_7'])
        costs['total'] += float(item['var_5']) + float(item['var_6']) + float(item['var_7'])

    # Debugging Purposes
    # print(costs)
    # print("\n")

    #======================#
    # CALCULATE SCENERIO 1 #
    #======================#
    # Calculate with a 25% decrease.
    scenerio1_revenue = scalar_multiply_by(revenue, 0.75)
    scenerio1_cogs = scalar_multiply_by(cogs, 0.75)
    gross_profit = matrix_subtract_by(scenerio1_revenue, scenerio1_cogs)
    total_expenses = scalar_multiply_by(costs, 0.75)
    net_profit = matrix_subtract_by(gross_profit, total_expenses)

    # scenerio1_labour = scalar_multiply_by(labour, 0.75)
    # scenerio1_materials = scalar_multiply_by(materials, 0.75)
    # scenerio1_overhead = scalar_multiply_by(overhead, 0.75)

    print("REVENUE")
    print(scenerio1_revenue)
    print("\n\n")
    print("COGS")
    print(scenerio1_cogs)
    print("\n\n")
    print("GROSS PROFIT")
    print(gross_profit)
    print("\n\n")
    print("TOTAL EXPENSES")
    print(total_expenses)
    print("\n\n")
    print("NET PROFIT")
    print(net_profit)
    print("\n\n")

    # print("LABOUR")
    # print(scenerio1_labour)
    # print("\n\n")
    # print("MATERIALS")
    # print(scenerio1_materials)
    # print("\n\n")
    # print("OVERHEAD")
    # print(scenerio1_overhead)
    # print("\n\n")



    # Render the template.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'answer_picked': answer.content,
        'autogen': autogen
    }
