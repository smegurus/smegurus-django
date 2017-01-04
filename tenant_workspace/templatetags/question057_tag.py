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


@register.inclusion_tag('templatetags/question/template_057.html')
def render_question_type_057(workspace, module, node, question, answer):
    """
    Dependency:
    - QID: 
    """
    # For this particular document and module, find the previous questions.
    # q1_qid = int_or_none(question.dependency['q1_qid'])
    # q2_qid = int_or_none(question.dependency['q2_qid'])
    # q3_qid = int_or_none(question.dependency['q3_qid'])
    # q4_qid = int_or_none(question.dependency['q4_qid'])
    #
    # # Fetch Q1
    # q1 = QuestionAnswer.objects.get(
    #     question_id=q1_qid,
    #     workspace=workspace
    # )
    # q1_picked = q1.content
    #
    # # Fetch Q2
    # q2 = QuestionAnswer.objects.get(
    #     question_id=q2_qid,
    #     workspace=workspace
    # )
    # q2_picked = q2.content
    #
    # # Fetch Q3
    # q3 = QuestionAnswer.objects.get(
    #     question_id=q3_qid,
    #     workspace=workspace
    # )
    # q3_picked = q3.content
    #
    # # Fetch Q4
    # q4 = QuestionAnswer.objects.get(
    #     question_id=q4_qid,
    #     workspace=workspace
    # )
    # q4_picked = q4.content
    #
    # # Calculate annual totals.
    # total_yr1 = 0.0
    # total_yr2 = 0.0
    # total_yr3 = 0.0
    # for item in q1_picked:
    #     total_yr1 += float(item['var_6'])
    #     total_yr2 += float(item['var_7'])
    #     total_yr3 += float(item['var_8'])
    # for item in q2_picked:
    #     total_yr1 += float(item['var_6'])
    #     total_yr2 += float(item['var_7'])
    #     total_yr3 += float(item['var_8'])
    # for item in q3_picked:
    #     total_yr1 += float(item['var_6'])
    #     total_yr2 += float(item['var_7'])
    #     total_yr3 += float(item['var_8'])
    # for item in q4_picked:
    #     total_yr1 += float(item['var_7'])
    #     total_yr2 += float(item['var_8'])
    #     total_yr3 += float(item['var_9'])
    #
    # autogen = {
    #     # --- YEAR 1 ---
    #     'yr_1': total_yr1,
    #     'm_01': total_yr1 / 12.00,
    #     'm_02': total_yr1 / 12.00,
    #     'm_03': total_yr1 / 12.00,
    #     'm_04': total_yr1 / 12.00,
    #     'm_05': total_yr1 / 12.00,
    #     'm_06': total_yr1 / 12.00,
    #     'm_07': total_yr1 / 12.00,
    #     'm_08': total_yr1 / 12.00,
    #     'm_09': total_yr1 / 12.00,
    #     'm_10': total_yr1 / 12.00,
    #     'm_11': total_yr1 / 12.00,
    #     'm_12': total_yr1 / 12.00,
    #
    #     # --- YEAR 2 ---
    #     'yr_2': total_yr2,
    #     'm_13': total_yr2 / 12.00,
    #     'm_14': total_yr2 / 12.00,
    #     'm_15': total_yr2 / 12.00,
    #     'm_16': total_yr2 / 12.00,
    #     'm_17': total_yr2 / 12.00,
    #     'm_18': total_yr2 / 12.00,
    #     'm_19': total_yr2 / 12.00,
    #     'm_20': total_yr2 / 12.00,
    #     'm_21': total_yr2 / 12.00,
    #     'm_22': total_yr2 / 12.00,
    #     'm_23': total_yr2 / 12.00,
    #     'm_24': total_yr2 / 12.00,
    #
    #     # --- YEAR 3 ---
    #     'yr_3': total_yr3,
    #     'm_25': total_yr3 / 12.00,
    #     'm_26': total_yr3 / 12.00,
    #     'm_27': total_yr3 / 12.00,
    #     'm_28': total_yr3 / 12.00,
    #     'm_29': total_yr3 / 12.00,
    #     'm_30': total_yr3 / 12.00,
    #     'm_31': total_yr3 / 12.00,
    #     'm_32': total_yr3 / 12.00,
    #     'm_33': total_yr3 / 12.00,
    #     'm_34': total_yr3 / 12.00,
    #     'm_35': total_yr3 / 12.00,
    #     'm_36': total_yr3 / 12.00
    # }

    # Render the template.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'answer_picked': answer.content,
        # 'autogen': autogen
    }
