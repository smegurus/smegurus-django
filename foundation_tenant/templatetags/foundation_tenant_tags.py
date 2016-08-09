# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from django.contrib.auth.models import User
from foundation_tenant.models.message import Message
# from foundation import constants


register = template.Library()


@register.simple_tag
def count_unread_messages(me_id):
    return Message.objects.filter(
        recipient=me_id,
        participants=me_id,
        date_read=None,
    ).distinct('participants').count()
