# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from smegurus import constants


register = template.Library()


@register.simple_tag
def reverse_previous_slide(workspace, module, slide):
    # if slide.previous_exercise_id > 0:  #TODO: IMPLEMENT
    #     return reverse('tenant_workspace_module_master', args=[workspace.id, module.id,])

    if slide.previous_slide_id > 0:
        return reverse('tenant_workspace_module_detail', args=[workspace.id, module.id, slide.previous_slide_id,])
    else:
        return reverse('tenant_workspace_module_start_master', args=[workspace.id, module.id,])


@register.simple_tag
def reverse_next_slide(workspace, module, slide):
    # CASE 1 of 3: Generate EXERCISE url.
    if slide.next_exercise_id > 0:
        return reverse('tenant_workspace_exercise_master', args=[workspace.id, slide.next_exercise_id])

    # CASE 2 of 3: Generate next SLIDE url.
    if slide.next_slide_id > 0:
        return reverse('tenant_workspace_module_detail', args=[workspace.id, module.id, slide.next_slide_id,])
    # CASE 3 of 3: Generate FINISH MODULE url.
    else:
        return reverse('tenant_workspace_module_finish_master', args=[workspace.id, module.id,])
