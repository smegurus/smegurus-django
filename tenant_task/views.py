from django.utils import timezone
from datetime import datetime, timedelta
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
from foundation_tenant.utils import int_or_none
from foundation_tenant.forms.tagform import TagForm
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.note import Note
from foundation_tenant.models.task import Task
from foundation_tenant.models.calendarevent import CalendarEvent
from foundation_tenant.models.inforesource import InfoResource
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
# @condition(last_modified_func=my_last_modified_func)
def task_open_master_page(request):
    tasks = Task.objects.filter(
        Q(assigned_by=request.tenant_me) |
        Q(opening=request.tenant_me)
    ).distinct('id')
    return render(request, 'tenant_task/master/view.html',{
        'page': 'tasks',
        'sub_page': 'open',
        'tasks': tasks,
    })


@login_required(login_url='/en/login')
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
# @condition(last_modified_func=my_last_modified_func)
def task_closed_master_page(request):
    tasks = Task.objects.filter(
        status=constants.CLOSED_TASK_STATUS,
    )
    return render(request, 'tenant_task/master/view.html',{
        'page': 'tasks',
        'sub_page': 'complete',
        'tasks': tasks,
    })


@login_required(login_url='/en/login')
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
# @condition(last_modified_func=my_last_modified_func)
def task_master_create_page(request):
    return render(request, 'tenant_task/create/view.html',{
        'page': 'tasks',
        'sub_page': 'create',
        'type_of': int_or_none(request.GET.get('type_of')),
        'all_profiles': TenantMe.objects.all(),
        'tags': Tag.objects.filter(is_program=True),
    })


@login_required(login_url='/en/login')
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
# @condition(last_modified_func=my_last_modified_func)
def task_details_page(request, id):
    task = get_object_or_404(Task, pk=int(id))
    return render(request, 'tenant_task/details/edit/view.html',{
        # Required.
        'page': 'tasks',
        'task': task,
        # # Tags.
        # 'tags': Tag.objects.all(),
        # # CalendarEvent
        # 'calendar_items': CalendarEvent.objects.filter(start__gte=timezone.now()),
        # # Resources
        # 'resources': InfoResource.objects.all(),
        # # Members.
        # 'entrepreneurs': TenantMe.objects.filter(owner__groups__id=constants.ENTREPRENEUR_GROUP_ID),
        # 'mentors': TenantMe.objects.filter(owner__groups__id=constants.MENTOR_GROUP_ID),
        # 'advisors': TenantMe.objects.filter(owner__groups__id=constants.ADVISOR_GROUP_ID),
        # 'managers': TenantMe.objects.filter(owner__groups__id=constants.ORGANIZATION_MANAGER_GROUP_ID),
        # 'admins': TenantMe.objects.filter(owner__groups__id=constants.ORGANIZATION_ADMIN_GROUP_ID),
    })
