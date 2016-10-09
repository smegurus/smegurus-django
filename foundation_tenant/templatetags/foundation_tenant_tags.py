# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from django.contrib.auth.models import User
from foundation_tenant.models.message import Message
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.task import Task
from foundation_tenant.utils import get_pretty_formatted_date
from smegurus import constants


register = template.Library()


@register.simple_tag
def count_unread_messages(me):
    return Message.objects.filter(
        recipient=me,
        participants=me,
        date_read=None,
    ).distinct('participants').count()


@register.simple_tag
def count_new_intakes():
    return Intake.objects.filter(
        Q(status=constants.PENDING_REVIEW_STATUS) | Q(status=constants.REJECTED_STATUS)
    ).count()


@register.filter
def is_note_protected(note):
    """
    Filter will return TRUE or FALSE depending on whether this Note is being
    referenced anywhere else.
    """
    try:
        Intake.objects.get(judgement_note=note)
        Intake.objects.get(privacy_note=note)
        Intake.objects.get(terms_note=note)
        Intake.objects.get(confidentiality_note=note)
        Intake.objects.get(collection_note=note)
        return True
    except Intake.DoesNotExist:
        pass

    return False


@register.simple_tag
def count_pending_tasks(me):
    return Task.objects.filter(
        Q(
            opening=me,
            status=constants.OPEN_TASK_STATUS,
        )
    ).count()


@register.filter
def pretty_formatted_date(date):
    return get_pretty_formatted_date(date)
