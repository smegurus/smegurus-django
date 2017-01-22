# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from django.contrib.auth.models import User
from foundation_tenant.models.base.message import Message
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.task import Task
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.me import TenantMe
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.utils import get_pretty_formatted_date
from smegurus import constants


register = template.Library()


@register.inclusion_tag('templatetags/notification_widget.html')
def render_notification_widget(me, notification):
    return {
        'notification': notification,
        'me': me
    }


@register.inclusion_tag('templatetags/pending_tasks_widget.html')
def render_pending_tasks_widget(me):
    pending_tasks_count = 0

    # Count the new intakes available to review.
    pending_intakes = Intake.objects.filter(
        Q(status=constants.PENDING_REVIEW_STATUS) | Q(status=constants.IN_REVIEW_STATUS)
    ).count()

    # Count taks that belong to me and I have to do.
    pending_tasks = Task.objects.filter(
        Q(
            opening=me,
            status=constants.OPEN_TASK_STATUS,
        )
    ).count()

    # Count pending documents to review.
    pending_document_reviews = Document.objects.filter(
        status=constants.DOCUMENT_PENDING_REVIEW_STATUS,
        workspace__mes__managed_by__id=me.id
    ).count()

    if me.is_org_admin():
        pending_tasks_count = pending_intakes + pending_tasks

    elif me.is_manager():
        pending_tasks_count = pending_intakes + pending_tasks + pending_document_reviews

    elif me.is_advisor():
        pending_tasks_count = pending_tasks + pending_document_reviews

    if me.is_entrepreneur():
        pending_tasks_count = pending_tasks

    return {
        'me': me,
        'pending_tasks_count': pending_tasks_count
    }


@register.inclusion_tag('templatetags/unread_messages_count_widget.html')
def render_unread_messages_count_widget(me):
    unread_messages_count = Message.objects.filter(
        recipient=me,
        participants=me,
        date_read=None,
    ).distinct('participants').count()
    return {
        'unread_messages_count': unread_messages_count
    }


@register.inclusion_tag('templatetags/entrepreneurs_aggregate_widget.html')
def render_entrepreneurs_aggregate_widget(me):
    title = None
    count = 0

    if me.is_org_admin():
        title = "Total Clients"
        count = TenantMe.objects.filter(owner__groups__id=constants.ENTREPRENEUR_GROUP_ID).count()

    elif me.is_manager():
        title = "Total Clients"
        count = TenantMe.objects.filter(owner__groups__id=constants.ENTREPRENEUR_GROUP_ID).count()

    elif me.is_advisor():
        title = "Total Assigned Clients"
        count = TenantMe.objects.filter(
            owner__groups__id=constants.ENTREPRENEUR_GROUP_ID,
            managed_by=me
        ).count()

    if me.is_entrepreneur():
        title = "Stage Level"
        count = me.stage_num

    return {
        'count': count,
        'title': title
    }


@register.inclusion_tag('templatetags/custom_datetime_widget.html')
def render_custom_datetime_widget(time_zone):
    return {
        'time_zone': 'time_zone'
    }


@register.inclusion_tag('templatetags/tags_widget.html')
def render_tags_widget(me):
    tags = Tag.objects.all()
    #TODO: Implement.
    return {
        'me': 0,
        'tags': tags
    }


@register.inclusion_tag('templatetags/progress_widget.html')
def render_progress_widget(me):
    return {
        'me': me,
        'percent': 50
    }


@register.inclusion_tag('templatetags/unread_messages_widget.html')
def render_unread_messages_widget(me):
    # Fetch all the Messages and only get a single message per sender. Also ensure
    # that deleted messages are not returned.
    messages = Message.objects.filter(
        recipient=me,
        participants=me
    ).distinct('participants')
    return {
        'me': me,
        'messages': messages,
    }


@register.inclusion_tag('templatetags/custom_calendar_widget.html')
def render_custom_calendar_widget(me):
    return {
        'me': me
    }
