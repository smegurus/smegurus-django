from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import condition
from foundation_public.utils import resolve_full_url_with_subdmain
from foundation_tenant.models.base.me import TenantMe
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.message import Message
from foundation_tenant.models.base.note import Note
from foundation_tenant.models.base.task import Task
from foundation_tenant.models.base.logevent import SortedLogEventByCreated
from foundation_tenant.models.base.commentpost import SortedCommentPostByCreated
from foundation_tenant.models.base.calendarevent import CalendarEvent
from foundation_tenant.models.bizmula.document import Document
from smegurus.settings import env_var
from smegurus import constants


# def latest_intake_details(request, id):
#     try:
#         return Intake.objects.filter(id=id).latest("last_modified").last_modified
#     except Intake.DoesNotExist:
#         return datetime.now()


@login_required(login_url='/en/login')
# @condition(last_modified_func=latest_intake_details)
def pending_intake_page(request, id):
    # Fetch the data.
    template_url = 'tenant_intake/pending_intake.html'
    intake = get_object_or_404(Intake, pk=int(id))
    url =  resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'tenant_intake_employee_details',
        [intake.id,]
    )
    web_view_extra_url = resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'foundation_email_pending_intake',
        [intake.id,]
    )

    # Run a security check to verify that the authenticated User is an employee
    # of the Organization.
    if not request.tenant_me.is_employee():
        raise PermissionDenied

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'intake': intake,
        'url': url,
        'web_view_url': web_view_extra_url
    })


@login_required(login_url='/en/login')
# @condition(last_modified_func=latest_intake_details)
def approved_intake_page(request, id):
    # Fetch the data.
    template_url = 'tenant_intake/approved_intake.html'
    intake = get_object_or_404(Intake, pk=int(id))
    url =  resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'foundation_auth_user_login',
        []
    )
    web_view_extra_url = resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'foundation_email_pending_intake',
        [intake.id,]
    )

    # Run a security check to verify that the authenticated User belongs to
    # the the Intake.
    if request.user != intake.me.owner:
        raise PermissionDenied

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'intake': intake,
        'url': url,
        'web_view_url': web_view_extra_url
    })


@login_required(login_url='/en/login')
# @condition(last_modified_func=latest_intake_details)
def rejected_intake_page(request, id):
    # Fetch the data.
    template_url = 'tenant_intake/rejected_intake.html'
    intake = get_object_or_404(Intake, pk=int(id))
    url =  resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'foundation_auth_user_login',
        []
    )
    web_view_extra_url = resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'foundation_email_rejected_intake',
        [intake.id,]
    )

    # Run a security check to verify that the authenticated User belongs to
    # the the Intake.
    if request.user != intake.me.owner:
        raise PermissionDenied

    # Render our email templated message.
    return render(request, template_url, {
        'user': request.user,
        'intake': intake,
        'url': url,
        'web_view_url': web_view_extra_url
    })


def latest_message_details(request, id):
    try:
        return Message.objects.get(pk=int(id)).last_modified
    except Message.DoesNotExist:
        return datetime.now()


@login_required(login_url='/en/login')
# @condition(last_modified_func=latest_message_details)
def message_page(request, id):
    # Fetch the data.
    template_url = 'tenant_message/message.html'
    message = get_object_or_404(Message, pk=int(id))
    url =  resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'tenant_conversation',
        [message.sender.id,]
    )
    web_view_extra_url = resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'foundation_email_message',
        [message.id,]
    )

    # Run a security check to make sure the authenticated User is a
    # participant in the conversation.
    if request.tenant_me not in message.participants.all():
        raise PermissionDenied

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'message': message,
        'url': url,
        'web_view_url': web_view_extra_url
    })


def latest_task_details(request, id):
    try:
        return Message.objects.get(pk=int(id)).last_modified
    except Message.DoesNotExist:
        return datetime.now()


@login_required(login_url='/en/login')
# @condition(last_modified_func=latest_task_details)
def task_page(request, task_id, log_event_id):
    # Fetch the data.
    template_url = 'tenant_task/task.html'
    task = get_object_or_404(Task, pk=int(task_id))
    log_event = get_object_or_404(SortedLogEventByCreated, pk=int(log_event_id))
    url =  resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'tenant_task_details_info',
        [task.id,]
    )
    web_view_extra_url = resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'foundation_email_task',
        [task.id, log_event.id,]
    )

    # Run a security check to make sure the authenticated User is a
    # participant in the conversation.
    if request.tenant_me not in task.participants.all():
        raise PermissionDenied

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'task': task,
        'log_event': log_event,
        'url': url,
        'web_view_url': web_view_extra_url
    })


@login_required(login_url='/en/login')
# @condition(last_modified_func=latest_task_details)
def calendar_pending_event_page(request, calendar_event_id):
    # Fetch the data.
    template_url = 'tenant_calendar/pending_invite.html'
    calendar_event = get_object_or_404(CalendarEvent, pk=int(calendar_event_id))
    url =  resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'tenant_calendar_details_info',
        [calendar_event.id,]
    )
    web_view_extra_url = resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'foundation_email_calendar_pending_event',
        [calendar_event.id,]
    )

    # # Run a security check to make sure the authenticated User is a
    # # participant in the conversation.
    # if request.tenant_me not in task.participants.all():
    #     raise PermissionDenied

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'me': request.tenant_me,
        'calendar_event': calendar_event,
        'url': url,
        'web_view_url': web_view_extra_url
    })


@login_required(login_url='/en/login')
# @condition(last_modified_func=latest_intake_details)
def pending_document_page(request, document_id):
    # Fetch the data.
    template_url = 'tenant_review/pending_doc_review.html'
    document = get_object_or_404(Document, pk=int(document_id))
    url =  resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'tenant_review_detail',
        [document.id,]
    )
    web_view_extra_url = resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'foundation_email_pending_document',
        [document.id,]
    )

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'document': document,
        'url': url,
        'web_view_url': web_view_extra_url,
    })


@login_required(login_url='/en/login')
# @condition(last_modified_func=latest_intake_details)
def rejected_document_page(request, document_id):
    # Fetch the data.
    template_url = 'tenant_review/rejected_doc_review.html'
    document = get_object_or_404(Document, pk=int(document_id))
    url =  resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'foundation_auth_user_login',
        []
    )
    web_view_extra_url = resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'foundation_email_rejected_document',
        [document.id,]
    )

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'document': document,
        'url': url,
        'web_view_url': web_view_extra_url,
    })


@login_required(login_url='/en/login')
# @condition(last_modified_func=latest_intake_details)
def accepted_document_page(request, document_id):
    # Fetch the data.
    template_url = 'tenant_review/accepted_doc_review.html'
    document = get_object_or_404(Document, pk=int(document_id))
    url =  resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'foundation_auth_user_login',
        []
    )
    web_view_extra_url = resolve_full_url_with_subdmain(
        request.tenant.schema_name,
        'foundation_email_accepted_document',
        [document.id,]
    )

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'document': document,
        'url': url,
        'web_view_url': web_view_extra_url,
    })
