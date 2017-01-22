from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.utils.translation import get_language
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from tenant_configuration.decorators import tenant_configuration_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.base.notification import Notification
from foundation_tenant.models.base.task import Task
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def dashboard_page(request):
    # Fetch the latest notification for the User.
    try:
        notification = Notification.objects.latest('created')
    except Exception as e:
        notification = None

    pending_tasks = Task.objects.filter(
        status=constants.OPEN_TASK_STATUS,
        opening__id=request.tenant_me.id
    )

    # Render the User.
    if request.tenant_me.is_org_admin():
        return admin_dashboard_page(request, notification, pending_tasks)

    elif request.tenant_me.is_manager():
        return org_manager_dashboard_page(request, notification, pending_tasks)

    elif request.tenant_me.is_advisor():
        return advisor_dashboard_page(request, notification, pending_tasks)

    if request.tenant_me.is_entrepreneur():
        return entrepreneur_dashboard_page(request, notification, pending_tasks)

    else:
        return HttpResponseBadRequest(_('You do not belong to any group!'))


def admin_dashboard_page(request, notification, pending_tasks):
    return render(request, 'dashboard/view.html',{
        'page': 'dashboard',
        'notification': notification,
        'pending_tasks': pending_tasks
    })


def org_manager_dashboard_page(request, notification, pending_tasks):
    return render(request, 'dashboard/view.html',{
        'page': 'dashboard',
        'notification': notification,
        'pending_tasks': pending_tasks
    })


def advisor_dashboard_page(request, notification, pending_tasks):
    return render(request, 'dashboard/view.html',{
        'page': 'dashboard',
        'notification': notification,
        'pending_tasks': pending_tasks
    })


def entrepreneur_dashboard_page(request, notification, pending_tasks):
    return render(request, 'dashboard/view.html',{
        'page': 'dashboard',
        'notification': notification,
        'pending_tasks': pending_tasks
    })
