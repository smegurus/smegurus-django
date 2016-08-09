# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from django.contrib.auth.models import User
from foundation_tenant.models.message import Message
from foundation_tenant.models.intake import Intake
from smegurus import constants


register = template.Library()


@register.simple_tag
def count_unread_messages(me_id):
    return Message.objects.filter(
        recipient=me_id,
        participants=me_id,
        date_read=None,
    ).distinct('participants').count()


@register.simple_tag
def count_new_intakes():
    return Intake.objects.filter(
        Q(status=constants.PENDING_REVIEW_STATUS) | Q(status=constants.REJECTED_STATUS)
        # | Q(status=constants.APPROVED_STATUS)
    ).count()
