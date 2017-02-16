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


@register.inclusion_tag('templatetags/question/template_062.html')
def render_question_type_062(workspace, module, node, question, answer):
    """
    Dependency:
    - Q99 | Total Sales Volume
    - Q100
    """
    # For this particular document and module, find the previous questions.
    # q1_qid = int_or_none(question.dependency['q1_qid'])
    # q2_qid = int_or_none(question.dependency['q2_qid'])
    # expenses = QuestionAnswer.objects.get(
    #     question_id=q1_qid,
    #     workspace=workspace
    # )

    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        # 'expenses': expenses,
        # 'volumes': volumes,
        # 'autogen': autogen
    }
