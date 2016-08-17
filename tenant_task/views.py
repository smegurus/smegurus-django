from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.views.decorators.http import condition
from django.db.models import Q
from rest_framework.authtoken.models import Token
from tenant_intake.decorators import tenant_intake_required
from tenant_profile.decorators import tenant_profile_required
from tenant_configuration.decorators import tenant_configuration_required
from smegurus import constants
from foundation_tenant.forms.tagform import TagForm
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.note import Note
from foundation_tenant.models.task import Task


def latest_task_master(request):
    try:
        return Task.objects.filter(participants=request.tenant_me).latest("last_modified").last_modified
    except Task.DoesNotExist:
        return datetime.now()


def latest_task_details(request, id):
    try:
        return Task.objects.get(id=int(id)).last_modified
    except Task.DoesNotExist:
        return datetime.now()


@login_required(login_url='/en/login')
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
@condition(last_modified_func=latest_task_master)
def task_master_page(request):
    tasks = Task.objects.filter(participants=request.tenant_me)
    return render(request, 'tenant_task/master/view.html',{
        'page': 'tasks',
        'tasks': tasks,
    })


@login_required(login_url='/en/login')
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
@condition(last_modified_func=latest_task_details)
def task_details_page(request, id):
    task = get_object_or_404(Task, pk=int(id))
    return render(request, 'tenant_task/details/view.html',{
        # Required.
        'page': 'tasks',
        'task': task,
        # Tags.
        'tags': Tag.objects.all(),
        # Members.
        'entrepreneurs': TenantMe.objects.filter(owner__groups__id=constants.ENTREPRENEUR_GROUP_ID),
        'mentors': TenantMe.objects.filter(owner__groups__id=constants.MENTOR_GROUP_ID),
        'advisors': TenantMe.objects.filter(owner__groups__id=constants.ADVISOR_GROUP_ID),
        'managers': TenantMe.objects.filter(owner__groups__id=constants.ORGANIZATION_MANAGER_GROUP_ID),
        'admins': TenantMe.objects.filter(owner__groups__id=constants.ORGANIZATION_ADMIN_GROUP_ID),
    })
