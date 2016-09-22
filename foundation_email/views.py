from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import condition
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.message import Message
from foundation_tenant.models.note import Note
from foundation_tenant.models.task import Task
from foundation_tenant.models.logevent import SortedLogEventByCreated
from foundation_tenant.models.commentpost import SortedCommentPostByCreated
from foundation_tenant.models.calendarevent import CalendarEvent
from smegurus.settings import env_var
from smegurus import constants


def get_url_with_subdmain(request, additonal_url=None):
    """Function will return the URL to the login page through the sub-domain of the organization."""
    url = 'https://' if request.is_secure() else 'http://'
    url += request.tenant.schema_name + "."
    url += get_current_site(request).domain
    if additonal_url:
        url += additonal_url
        url = url.replace("/None/","/en/")
    return url


def get_login_url(request):
    """Function will return the URL to the login page through the sub-domain of the organization."""
    url = 'https://' if request.is_secure() else 'http://'
    url += request.tenant.schema_name + "."
    url += get_current_site(request).domain
    url += reverse('foundation_auth_user_login')
    url = url.replace("/None/","/en/")
    return url


def get_message_url(request, message):
    url = 'https://' if request.is_secure() else 'http://'
    url += request.tenant.schema_name + "."
    url += get_current_site(request).domain
    url += reverse('tenant_conversation', args=[message.sender.id,])
    url = url.replace("None","en")
    return url


def get_task_url(request, task):
    url = 'https://' if request.is_secure() else 'http://'
    url += request.tenant.schema_name + "."
    url += get_current_site(request).domain
    url += reverse('tenant_task_details', args=[task.id,])
    url = url.replace("None","en")
    return url


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
    url = reverse('tenant_intake_employee_details', args=[intake.id,])
    web_view_extra_url = reverse('foundation_email_pending_intake', args=[intake.id,])

    # Run a security check to verify that the authenticated User is an employee
    # of the Organization.
    if not request.tenant_me.is_employee():
        raise PermissionDenied

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'intake': intake,
        'url': get_url_with_subdmain(request, url),
        'web_view_url': get_url_with_subdmain(request, web_view_extra_url),
    })


@login_required(login_url='/en/login')
# @condition(last_modified_func=latest_intake_details)
def approved_intake_page(request, id):
    # Fetch the data.
    template_url = 'tenant_intake/approved_intake.html'
    intake = get_object_or_404(Intake, pk=int(id))
    web_view_extra_url = reverse('foundation_email_approved_intake', args=[intake.id,])

    # Run a security check to verify that the authenticated User belongs to
    # the the Intake.
    if request.user != intake.me.owner:
        raise PermissionDenied

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'intake': intake,
        'url': get_login_url(request),
        'web_view_url': get_url_with_subdmain(request, web_view_extra_url),
    })


@login_required(login_url='/en/login')
# @condition(last_modified_func=latest_intake_details)
def rejected_intake_page(request, id):
    # Fetch the data.
    template_url = 'tenant_intake/rejected_intake.html'
    intake = get_object_or_404(Intake, pk=int(id))
    web_view_extra_url = reverse('foundation_email_rejected_intake', args=[intake.id,])

    # Run a security check to verify that the authenticated User belongs to
    # the the Intake.
    if request.user != intake.me.owner:
        raise PermissionDenied

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'intake': intake,
        'url': get_login_url(request),
        'web_view_url': get_url_with_subdmain(request, web_view_extra_url),
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
    web_view_extra_url = reverse('foundation_email_message', args=[message.id,])

    # Run a security check to make sure the authenticated User is a
    # participant in the conversation.
    if request.tenant_me not in message.participants.all():
        raise PermissionDenied

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'message': message,
        'url': get_message_url(request, message),
        'web_view_url': get_url_with_subdmain(request, web_view_extra_url),
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
    web_view_extra_url = reverse('foundation_email_task', args=[task.id, log_event.id,])

    # Run a security check to make sure the authenticated User is a
    # participant in the conversation.
    if request.tenant_me not in task.participants.all():
        raise PermissionDenied

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'task': task,
        'log_event': log_event,
        'url': get_task_url(request, task),
        'web_view_url': get_url_with_subdmain(request, web_view_extra_url),
    })


def get_calendar_info_url(request, calendar_event):
    url = 'https://' if request.is_secure() else 'http://'
    url += request.tenant.schema_name + "."
    url += get_current_site(request).domain
    url += reverse('tenant_calendar_details_info', args=[calendar_event.id,])
    url = url.replace("None","en")
    return url


@login_required(login_url='/en/login')
# @condition(last_modified_func=latest_task_details)
def calendar_pending_event_page(request, calendar_event_id):
    # Fetch the data.
    template_url = 'tenant_calendar/pending_invite.html'
    calendar_event = get_object_or_404(CalendarEvent, pk=int(calendar_event_id))

    web_view_extra_url = reverse('foundation_email_calendar_pending_event', args=[calendar_event.id,])

    # # Run a security check to make sure the authenticated User is a
    # # participant in the conversation.
    # if request.tenant_me not in task.participants.all():
    #     raise PermissionDenied

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'me': request.tenant_me,
        'calendar_event': calendar_event,
        'url': get_calendar_info_url(request, calendar_event),
        'web_view_url': get_url_with_subdmain(request, web_view_extra_url),
    })
