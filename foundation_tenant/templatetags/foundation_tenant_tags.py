# -*- coding: utf-8 -*-
from django import template
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import resolve, reverse # Reverse
from foundation_public import constants
from foundation_tenant.models.me import TenantMe
from smegurus.settings import env_var


register = template.Library()


@register.simple_tag
def is_employee(me):
    for my_group in me.owner.groups.all():
        for employee_group_id in constants.EMPLOYEE_GROUP_IDS:
            if employee_group_id == my_group.id:
                return True
    return False
