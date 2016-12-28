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


@register.inclusion_tag('templatetags/question/template_049.html')
def render_question_type_049(workspace, module, node, question, answer):
    """
    Dependency:
    - QID: 77 | I will offer the the following incentives to get customers to try my products or services
    - QID: 78 | I will use the following physical marketing materials as ways to communicate my product or service to customers
    - QID: 79 | I will reach my customers through the following media campaigns
    - QID: 80 | Working with others is a cost-effective way to grow. Cooperating can mean running campaigns together or even joint ventures. List up to 5 potential partnerships you can utilize to grow your company.
    """
    # For this particular document and module, find the previous questions.
    q1_qid = int_or_none(question.dependency['q1_qid'])
    q2_qid = int_or_none(question.dependency['q2_qid'])
    q3_qid = int_or_none(question.dependency['q3_qid'])
    q4_qid = int_or_none(question.dependency['q4_qid'])

    #TODO: Impl.

    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer
    }
