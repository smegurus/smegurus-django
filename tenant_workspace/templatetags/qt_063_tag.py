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


@register.inclusion_tag('templatetags/question/template_063.html')
def render_question_type_063(workspace, module, node, question, answer):
    """
    Dependency:
    - Q99 | Total Sales Volume
    - Q100
    """
    # For this particular document and module, find the previous questions.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    q2_qid = int_or_none(question.dependency['q2_qid'])
    q3_qid = int_or_none(question.dependency['q3_qid'])
    sales_volume = QuestionAnswer.objects.get(
        question_id=q1_qid,
        workspace=workspace
    )
    cogs_volume = QuestionAnswer.objects.get(
        question_id=q2_qid,
        workspace=workspace
    )
    total_sales = QuestionAnswer.objects.get(
        question_id=q3_qid,
        workspace=workspace
    )

    # Calculate Total COGS volume.
    total_cogs_volume = {
        'yr1': cogs_volume.content['total_cogs_yr1'] * sales_volume.content['yr1_total'],
        'yr2': cogs_volume.content['total_cogs_yr2'] * sales_volume.content['yr2_total'],
        'yr3': cogs_volume.content['total_cogs_yr3'] * sales_volume.content['yr3_total']
    }

    # Calculate gross profit.
    gross_profit = {
        'yr1': total_sales.content['yr1_total'] - total_cogs_volume['yr1'],
        'yr2': total_sales.content['yr2_total'] - total_cogs_volume['yr2'],
        'yr3': total_sales.content['yr3_total'] - total_cogs_volume['yr3']
    }

    # Save the answer content.
    answer.content = gross_profit
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
