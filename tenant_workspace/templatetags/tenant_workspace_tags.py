# -*- coding: utf-8 -*-
import json
from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from foundation_tenant.utils import int_or_none
from foundation_tenant.models.bizmula.question import Question
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer
from smegurus import constants


register = template.Library()


@register.simple_tag
def reverse_previous_node(workspace, module, node):
    if node['previous_position'] == -1:
        return reverse('tenant_workspace_module_start_master', args=[workspace.id, module.id,])
    else:
        return reverse('tenant_workspace_module_detail', args=[workspace.id, module.id, node['previous_position'],])


@register.simple_tag
def reverse_next_node(workspace, module, node):
    if node['next_position'] == -1:
        return reverse('tenant_workspace_module_finish_master', args=[workspace.id, module.id, 0])
    else:
        return reverse('tenant_workspace_module_detail', args=[workspace.id, module.id, node['next_position'],])


@register.inclusion_tag('templatetags/question/render_question_001.html')
def render_question_001(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/render_question_002.html')
def render_question_002(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/render_question_003.html')
def render_question_003(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/render_question_004.html')
def render_question_004(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        "OTHER_TEXT": "other"
    }


@register.inclusion_tag('templatetags/question/render_question_005.html')
def render_question_005(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/render_question_006.html')
def render_question_006(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/render_question_007.html')
def render_question_007(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/render_question_008.html')
def render_question_008(workspace, module, node, question, answer):
    picked = json.loads(answer.content)
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': picked,
        'picked_count': len(picked),
        "OTHER_TEXT": "Other (Please Specify)"
    }


@register.inclusion_tag('templatetags/question/render_question_009.html')
def render_question_009(workspace, module, node, question, answer):
    """
    Question will render results based on previously saved answer from a
    question that is formatted using "template_id" of 001.
    """
    # For this particular document and module, find the previous question.
    previous_question_id = int_or_none(question.dependency['previous_question_id'])
    previous_question_answer = get_object_or_404(QuestionAnswer, question_id=previous_question_id)

    # Input the variables into the template and render the view.
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content),  # Convert string to JSON dictionary.
        'previous_picked': json.loads(previous_question_answer.content),  # Convert string to JSON dictionary.
        "OTHER_TEXT": "Other (Please Specify)"
    }
