# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template import Library
from smegurus import constants


register = Library()


@register.simple_tag
def reverse_previous_question(workspace, exercise, question):
    previous_question_id = exercise.previous_question_id(question.id)
    if previous_question_id == question.id:
        return reverse('tenant_workspace_module_detail', args=[workspace.id, exercise.module.id, exercise.previous_slide_id])
    else:
        return reverse('tenant_workspace_exercise_detail', args=[workspace.id, exercise.id, previous_question_id])


@register.simple_tag
def reverse_next_question(workspace, exercise, question):
    next_question_id = exercise.next_question_id(question.id)
    if next_question_id == question.id:
        return reverse('tenant_workspace_module_detail', args=[workspace.id, exercise.module.id, exercise.next_slide_id])
    else:
        return reverse('tenant_workspace_exercise_detail', args=[workspace.id, exercise.id, next_question_id])


@register.inclusion_tag('templatetags/question/render_question_001.html')
def render_question_001(workspace, exercise, question):

    return {
        'test': ''
    }
