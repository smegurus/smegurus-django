from datetime import datetime
from django.core.signing import Signer
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
from foundation_tenant.models.orderedlogevent import OrderedLogEvent
from foundation_tenant.models.orderedcommentpost import OrderedCommentPost
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


def get_activation_url(request):
    # Convert our User's ID into an encrypted value.
    # Note: https://docs.djangoproject.com/en/dev/topics/signing/
    signer = Signer()
    id_sting = str(request.user.id).encode()
    value = signer.sign(id_sting)

    # Generate our site's URL.
    url = 'https://' if request.is_secure() else 'http://'
    schema_name = request.tenant.schema_name
    if schema_name == 'public' or schema_name == 'test':
        url += "www."
    else:
        url += schema_name + "."
    url += get_current_site(request).domain
    url += reverse('foundation_auth_user_activation', args=[value,])
    url = url.replace("None","en")
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


def user_last_login(request):
    return request.user.last_login


@login_required(login_url='/en/login')
@condition(last_modified_func=user_last_login)
def activate_page(request):
    # Get our template url depending on whether User is admin or not.
    template_url = 'foundation_auth/activate_org_admin.html'
    web_view_extra_url = reverse('foundation_email_activate')
    for my_group in request.user.groups.all():
        if constants.ENTREPRENEUR_GROUP_ID == my_group.id:
            template_url = 'foundation_auth/activate_entrepreneur.html'

    # Render our email templated message.
    return render(request, template_url,{
        'user': request.user,
        'url': get_activation_url(request),
        'web_view_url': get_url_with_subdmain(request, web_view_extra_url),
    })


def latest_intake_details(request, id):
    try:
        return Intake.objects.filter(id=id).latest("last_modified").last_modified
    except Intake.DoesNotExist:
        return datetime.now()


@login_required(login_url='/en/login')
@condition(last_modified_func=latest_intake_details)
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
@condition(last_modified_func=latest_intake_details)
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
@condition(last_modified_func=latest_intake_details)
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
@condition(last_modified_func=latest_message_details)
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
    log_event = get_object_or_404(OrderedLogEvent, pk=int(log_event_id))
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
