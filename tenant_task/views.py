from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.views.decorators.http import condition
from django.db.models import Q
from rest_framework.authtoken.models import Token
from foundation_tenant.utils import my_last_modified_func
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


@login_required(login_url='/en/login')
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
@condition(last_modified_func=my_last_modified_func)
def task_master_page(request):
    pending_tasks = Task.objects.filter(
        Q(
            participants=request.tenant_me,
            status=constants.UNASSIGNED_TASK_STATUS,
        ) | Q(
            participants=request.tenant_me,
            status=constants.ASSIGNED_TASK_STATUS,
        )
    )

    incomplete_tasks = Task.objects.filter(
        participants=request.tenant_me,
        status=constants.INCOMPLETE_TASK_STATUS,
    )

    completed_tasks = Task.objects.filter(
        participants=request.tenant_me,
        status=constants.COMPLETED_TASK_STATUS,
    )

    return render(request, 'tenant_task/master/view.html',{
        'page': 'tasks',
        'pending_tasks': pending_tasks,
        'incomplete_tasks': incomplete_tasks,
        'completed_tasks': completed_tasks,
    })


@login_required(login_url='/en/login')
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
@condition(last_modified_func=my_last_modified_func)
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
