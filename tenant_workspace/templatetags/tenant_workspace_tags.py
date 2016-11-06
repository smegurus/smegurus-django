# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer
from smegurus import constants


register = template.Library()


@register.simple_tag
def reverse_previous_node(workspace, module, node):
    if node['previous'] == -1:
        return reverse('tenant_workspace_module_start_master', args=[workspace.id, module.id,])
    else:
        return reverse('tenant_workspace_module_detail', args=[workspace.id, module.id, node['previous'],])


@register.simple_tag
def reverse_next_node(workspace, module, node):
    if node['next'] == -1:
        return reverse('tenant_workspace_module_finish_master', args=[workspace.id, module.id,])
    else:
        return reverse('tenant_workspace_module_detail', args=[workspace.id, module.id, node['next'],])


@register.inclusion_tag('templatetags/question/render_question_001.html')
def render_question_001(workspace, module, node, question, answer):
    return {
        'workspace': workspace,
        'module': module,
        'node': node,
        'question': question,
        'answer': answer
    }
