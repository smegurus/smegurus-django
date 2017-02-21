# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from foundation_tenant.utils import int_or_none
from foundation_tenant.models.base.naicsoption import NAICSOption
from foundation_tenant.models.base.imageupload import ImageUpload
from foundation_tenant.models.bizmula.question import Question
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer
from smegurus import constants


def matrix_subtract_by(arr1, arr2):
    return {
        'yr1': arr1['yr1'] - arr2['yr1'],
        "yr2": arr1['yr2'] - arr2['yr2'],
        "yr3": arr1['yr3'] - arr2['yr3'],
        "total": arr1['total'] - arr2['total']
    }


def matrix_divide_by(arr1, arr2):
    computation = {}
    try:
        computation['yr1'] = arr1['yr1'] / arr2['yr1'],
    except Exception as e:
        computation['yr1'] = 0

    try:
        computation['yr2'] = arr1['yr2'] / arr2['yr2'],
    except Exception as e:
        computation['yr1'] = 0

    try:
        computation['yr3'] = arr1['yr3'] / arr2['yr3'],
    except Exception as e:
        computation['yr3'] = 0

    try:
        computation['total'] = arr1['total'] / arr2['total']
    except Exception as e:
        computation['total'] = 0

    return computation


register = template.Library()


@register.inclusion_tag('templatetags/question/template_065.html')
def render_question_type_065(workspace, module, node, question, answer):
    # ALGORITHM
    # {{contribution_margin_unit_y1}} equals ({{total_sales_y1}}  - {{total_variable_costs_y1}}) / {{unit_sales_y1_total}}
    # {{contribution_margin_unit_y3}} equals ({{total_sales_y2}}  - {{total_variable_costs_y2}}) / {{unit_sales_y2_total}}
    # {{contribution_margin_unit_y3}} equals ({{total_sales_y3}}  - {{total_variable_costs_y3}}) / {{unit_sales_y3_total}}

    # For this particular document and module, find the previous questions.
    q1_qid = int_or_none(question.dependency['q1_qid']) # 99  | unit_sales_yr123_total
    q2_qid = int_or_none(question.dependency['q2_qid']) # 163 | total sales_yr123
    q3_qid = int_or_none(question.dependency['q3_qid']) # 165 | total_fixed_costs_yr123 & total_variable_costs_yr123

    # Fetch the questions.
    q1 = QuestionAnswer.objects.get(
        question_id=q1_qid,
        workspace=workspace
    )
    q1_picked = q1.content
    q2 = QuestionAnswer.objects.get(
        question_id=q2_qid,
        workspace=workspace
    )
    q2_picked = q2.content
    q3 = QuestionAnswer.objects.get(
        question_id=q3_qid,
        workspace=workspace
    )
    q3_picked = q3.content

    # DEBUGGING PURPOSES ONLY
    # print(q1_picked)
    # print("\n\n")
    # print(q2_picked)
    # print("\n\n")
    # print(q3_picked)
    # print("\n\n")

    #================================#
    # Total Contribution Margin (CM) #
    #================================#

    # Get our first step.
    unit_sales = {
        'yr1': q1_picked['yr1_total'],
        'yr2': q1_picked['yr2_total'],
        'yr3': q1_picked['yr3_total'],
        'total': q1_picked['yr1_total'] + q1_picked['yr2_total'] + q1_picked['yr3_total']
    }
    total_variable_costs = q3_picked['total_variable_costs']
    total_sales = {
        'yr1': q2_picked['yr1_total'],
        'yr2': q2_picked['yr2_total'],
        'yr3': q2_picked['yr3_total'],
        'total': q2_picked['yr1_total'] + q2_picked['yr2_total'] + q2_picked['yr3_total']
    }

    # DEBUGGING PURPOSES
    # print(total_variable_costs)
    # print(total_sales)

    # Compute.
    contribution_margin = matrix_subtract_by(total_sales, total_variable_costs)

    # DEBUGGING PURPOSES
    # print(contribution_margin)

    # Compute.
    contribution_margin_unit = matrix_divide_by(contribution_margin, unit_sales)

    #===============================#
    # Total Breakeven in Units (BE) #
    #===============================#

    total_fixed_costs = q3_picked['total_fixed']

    # Compute.
    break_even_units = matrix_divide_by(contribution_margin_unit, total_fixed_costs)

    #=======#
    # Saved #
    #=======#

    answer.content = {
        'contribution_margin_unit': contribution_margin_unit,
        'break_even_units': break_even_units
    }
    answer.save()

    # DEBUGGING PURPOSES ONLY
    # print(answer.content)

    # Return result.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': answer.content,
    }
