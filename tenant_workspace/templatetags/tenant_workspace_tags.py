# -*- coding: utf-8 -*-
import json
from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
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
        'picked': json.loads(answer.content)
    }


@register.inclusion_tag('templatetags/question/render_question_002.html')
def render_question_002(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer,
        'picked': json.loads(answer.content)
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
        'picked_count': len(picked)
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
        'picked_count': len(picked)
    }
