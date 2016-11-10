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
def reception_reverse_previous_node(workspace, node):
    if node['previous_position'] == -1:
        return reverse('tenant_reception_workspace_start_master', args=[workspace.id,])
    else:
        return reverse('tenant_reception_workspace_detail', args=[workspace.id, node['previous_position'],])


@register.simple_tag
def reception_reverse_next_node(workspace, node):
    if node['next_position'] == -1:
        return reverse('tenant_reception_workspace_finish_master', args=[workspace.id, node['current_position'],])
    else:
        return reverse('tenant_reception_workspace_detail', args=[workspace.id, node['next_position'],])
