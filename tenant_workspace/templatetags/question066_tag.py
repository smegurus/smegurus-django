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


@register.inclusion_tag('templatetags/question/template_066.html')
def render_question_type_066(workspace, module, node, question, answer):

    #TODO: Implement.

    # Return result.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        # 'picked': answer.content,
    }
