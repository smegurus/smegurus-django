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

def get_inventory(q2, q5):
    total = 0.00
    index = q5['var_1']


    if index > 1:
        total += 1
    # print(q5)
    # print("------")
    # print(q2)
    return {} # startup_inventory_req


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
    #------------------
    # Assets Owned
    for item in q4:
        total_yr1 += float(item['var_5'])
        total_yr2 += float(item['var_6'])
        total_yr3 += float(item['var_7'])
    assets_owner = {
        'asset_y1_costs_total': total_yr1,
        'asset_y2_costs_total': total_yr2,
        'asset_y3_costs_total': total_yr3
    }

    # Cash Required
    #------------------
    # Assets to Purchase
    total_yr1 = 0.0
    total_yr2 = 0.0
    total_yr3 = 0.0
    for item in q1:
        total_yr1 += float(item['var_5'])
        total_yr2 += float(item['var_6'])
        total_yr3 += float(item['var_7'])
    assets_to_purchase = {
        'equipment_y1_costs': total_yr1,
        'equipment_y2_costs': total_yr2,
        'equipment_y3_costs': total_yr3
    }

    # Inventory
    startup_inventory_req = get_inventory(q2, q5)







    # Return result.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        # 'picked': answer.content,
    }
