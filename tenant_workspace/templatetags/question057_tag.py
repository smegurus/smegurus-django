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


def calculate_revenue(sales_price_per_unit, units_sold):
    return {
        'revenue_yr1': sales_price_per_unit['sales_per_unit_yr1'] * units_sold['yr1_total'],
        'revenue_yr2': sales_price_per_unit['sales_per_unit_yr2'] * units_sold['yr2_total'],
        'revenue_yr3': sales_price_per_unit['sales_per_unit_yr3'] * units_sold['yr3_total']
    }


def multiply_revenue_by(revenue, percent):
    revenue['revenue_yr1'] *= percent
    revenue['revenue_yr2'] *= percent
    revenue['revenue_yr3'] *= percent
    return revenue


@register.inclusion_tag('templatetags/question/template_057.html')
def render_question_type_057(workspace, module, node, question, answer):
    """
    ============================================================================
    Dependency:
    ============================================================================
    - QID: 100 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/4/   |
    - QID: 99  | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/3/   |
    - QID: 77  | http://mikasoftware.smegurus.xyz/en/workspace/3/module/4/17/  |
    - QID: 78  | http://mikasoftware.smegurus.xyz/en/workspace/3/module/4/18/  |
    - QID: 79  | http://mikasoftware.smegurus.xyz/en/workspace/3/module/4/19/  |
    - QID: 80  | http://mikasoftware.smegurus.xyz/en/workspace/3/module/4/20/  |
    - QID: 85  | http://mikasoftware.smegurus.xyz/en/workspace/3/module/5/5/   |
    - QID: 86  | http://mikasoftware.smegurus.xyz/en/workspace/3/module/5/6/   |
    - QID: 90  | http://mikasoftware.smegurus.xyz/en/workspace/3/module/5/10/  |
    - QID: 105 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/9/   |
    - QID: 108 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/12/  |
    - QID: 111 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/15/  |
    - QID: 114 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/18/  |
    - QID: 116 | http://mikasoftware.smegurus.xyz/en/workspace/3/module/6/20/  |
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

    # Calculate the revenue.
    revenue = calculate_revenue(q1_picked, q2_picked)
    # print(revenue)

    # Calculate revenue with a 25% decrease.
    revenue = multiply_revenue_by(revenue, 0.75)
    # print(revenue)

    #================#
    # CALCULATE COST #
    #================#

    costs = {
        "costs_yr1": 0,
        "costs_yr2": 0,
        "costs_yr3": 0
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
        costs['costs_yr1'] += float(item['var_6'])
        costs['costs_yr2'] += float(item['var_7'])
        costs['costs_yr3'] += float(item['var_8'])

    # Q4 - FETCH
    q4_qid = int_or_none(question.dependency['q4_qid'])
    q4 = QuestionAnswer.objects.get(
        question_id=q4_qid,
        workspace=workspace
    )
    q4_picked = q4.content

    # Q4 - CALCULATE SUM
    for item in q4_picked:
        costs['costs_yr1'] += float(item['var_6'])
        costs['costs_yr2'] += float(item['var_7'])
        costs['costs_yr3'] += float(item['var_8'])

    # Q5 - FETCH
    q5_qid = int_or_none(question.dependency['q5_qid'])
    q5 = QuestionAnswer.objects.get(
        question_id=q5_qid,
        workspace=workspace
    )
    q5_picked = q5.content

    # Q5 - CALCULATE SUM
    for item in q5_picked:
        costs['costs_yr1'] += float(item['var_6'])
        costs['costs_yr2'] += float(item['var_7'])
        costs['costs_yr3'] += float(item['var_8'])

    # Q6 - FETCH
    q6_qid = int_or_none(question.dependency['q6_qid'])
    q6 = QuestionAnswer.objects.get(
        question_id=q6_qid,
        workspace=workspace
    )
    q6_picked = q6.content

    # Q6 - CALCULATE SUM
    for item in q6_picked:
        costs['costs_yr1'] += float(item['var_7'])
        costs['costs_yr2'] += float(item['var_8'])
        costs['costs_yr3'] += float(item['var_9'])

    # Q7 - FETCH
    q7_qid = int_or_none(question.dependency['q7_qid'])
    q7 = QuestionAnswer.objects.get(
        question_id=q4_qid,
        workspace=workspace
    )
    q7_picked = q7.content

    # Q7 - CALCULATE SUM
    for item in q7_picked:
        costs['costs_yr1'] += float(item['var_6'])
        costs['costs_yr2'] += float(item['var_7'])
        costs['costs_yr3'] += float(item['var_8'])

    # Q8 - FETCH
    q8_qid = int_or_none(question.dependency['q8_qid'])
    q8 = QuestionAnswer.objects.get(
        question_id=q8_qid,
        workspace=workspace
    )
    q8_picked = q8.content

    # Q8 - CALCULATE SUM
    for item in q8_picked:
        costs['costs_yr1'] += float(item['var_5'])
        costs['costs_yr2'] += float(item['var_6'])
        costs['costs_yr3'] += float(item['var_7'])

    # Q9 - FETCH
    q9_qid = int_or_none(question.dependency['q9_qid'])
    q9 = QuestionAnswer.objects.get(
        question_id=q9_qid,
        workspace=workspace
    )
    q9_picked = q9.content

    # Q9 - CALCULATE SUM
    for item in q9_picked:
        costs['costs_yr1'] += float(item['var_5'])
        costs['costs_yr2'] += float(item['var_6'])
        costs['costs_yr3'] += float(item['var_7'])

    # Q10 - FETCH
    q10_qid = int_or_none(question.dependency['q10_qid'])
    q10 = QuestionAnswer.objects.get(
        question_id=q10_qid,
        workspace=workspace
    )
    q10_picked = q10.content

    # Q10 - CALCULATE SUM
    for item in q10_picked:
        costs['costs_yr1'] += float(item['var_5'])
        costs['costs_yr2'] += float(item['var_6'])
        costs['costs_yr3'] += float(item['var_7'])

    # Q11 - FETCH
    q11_qid = int_or_none(question.dependency['q11_qid'])
    q11 = QuestionAnswer.objects.get(
        question_id=q11_qid,
        workspace=workspace
    )
    q11_picked = q11.content

    # Q11 - CALCULATE SUM
    for item in q11_picked:
        costs['costs_yr1'] += float(item['var_5'])
        costs['costs_yr2'] += float(item['var_6'])
        costs['costs_yr3'] += float(item['var_7'])

    # Q12 - FETCH
    q12_qid = int_or_none(question.dependency['q12_qid'])
    q12 = QuestionAnswer.objects.get(
        question_id=q12_qid,
        workspace=workspace
    )
    q12_picked = q12.content

    # Q12 - CALCULATE SUM
    for item in q4_picked:
        costs['costs_yr1'] += float(item['var_6'])
        costs['costs_yr2'] += float(item['var_7'])
        costs['costs_yr3'] += float(item['var_8'])

    # Q13 - FETCH
    q13_qid = int_or_none(question.dependency['q13_qid'])
    q13 = QuestionAnswer.objects.get(
        question_id=q13_qid,
        workspace=workspace
    )
    q13_picked = q13.content

    # Q13 - CALCULATE SUM
    for item in q13_picked:
        costs['costs_yr1'] += float(item['var_5'])
        costs['costs_yr2'] += float(item['var_6'])
        costs['costs_yr3'] += float(item['var_7'])

    # Q14 - FETCH
    q14_qid = int_or_none(question.dependency['q14_qid'])
    q14 = QuestionAnswer.objects.get(
        question_id=q14_qid,
        workspace=workspace
    )
    q14_picked = q14.content

    # Q14 - CALCULATE SUM
    for item in q14_picked:
        costs['costs_yr1'] += float(item['var_5'])
        costs['costs_yr2'] += float(item['var_6'])
        costs['costs_yr3'] += float(item['var_7'])

    #===================#
    # CALCULATE OPTIONS #
    #===================#

    #TODO: Implement.

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
