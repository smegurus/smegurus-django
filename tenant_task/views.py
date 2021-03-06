from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.authtoken.models import Token
from tenant_intake.decorators import tenant_intake_required
from tenant_profile.decorators import tenant_profile_required
from tenant_configuration.decorators import tenant_configuration_required
from foundation_tenant.decorators import tenant_required
from foundation_tenant.utils import int_or_none
from foundation_tenant.forms.tagform import TagForm
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.note import Note
from foundation_tenant.models.base.task import Task
from foundation_tenant.models.base.calendarevent import CalendarEvent
from foundation_tenant.models.base.inforesource import InfoResource
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_required
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
def task_open_master_page(request):
    tasks = Task.objects.filter(
        Q(
            Q(status=constants.OPEN_TASK_STATUS) & Q(assigned_by=request.tenant_me)
        ) | Q(
            Q(opening=request.tenant_me)
        )
    ).distinct('id')
    return render(request, 'tenant_task/master/view.html',{
        'page': 'tasks',
        'sub_page': 'open',
        'tasks': tasks,
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
def task_closed_master_page(request):
    tasks = Task.objects.filter(
        Q(
            Q(status=constants.CLOSED_TASK_STATUS) & Q(assigned_by=request.tenant_me)
        ) | Q(
            Q(closures=request.tenant_me)
        )
    ).distinct('id')
    return render(request, 'tenant_task/master/view.html',{
        'page': 'tasks',
        'sub_page': 'complete',
        'tasks': tasks,
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
def task_master_create_page(request):
    return render(request, 'tenant_task/create/view.html',{
        'page': 'tasks',
        'sub_page': 'create',
        'type_of': int_or_none(request.GET.get('type_of')),
        'default_me': int_or_none(request.GET.get('default_me')),
        'all_profiles': Me.objects.all(),
        'tags': Tag.objects.filter(is_program=True),
        'inforesources': InfoResource.objects.all(),
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
def task_edit_details_page(request, id):
    task = get_object_or_404(Task, pk=int(id))
    return render(request, 'tenant_task/details/edit/view.html',{
        # Required.
        'page': 'tasks',
        'task': task,
        # Tags.
        'tags': Tag.objects.all(),
        # CalendarEvent
        'calendar_items': CalendarEvent.objects.filter(start__gte=timezone.now()),
        # Resources
        'inforesources': InfoResource.objects.all(),
        # Members.
        'all_profiles': Me.objects.all(),
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
def task_info_details_page(request, id):
    task = get_object_or_404(Task, pk=int(id))
    return render(request, 'tenant_task/details/edit/view.html',{
        # Required.
        'page': 'tasks',
        'task': task,
        # Tags.
        'tags': Tag.objects.all(),
        # CalendarEvent
        'calendar_items': CalendarEvent.objects.filter(start__gte=timezone.now()),
        # Resources
        'resources': InfoResource.objects.all(),
        # Members.
        'all_profiles': Me.objects.all(),
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
def task_info_details_page(request, id):
    task = get_object_or_404(Task, pk=int(id))
    return render(request, 'tenant_task/details/info/view.html',{
        # Required.
        'page': 'tasks',
        'task': task,
        # Tags.
        'tags': Tag.objects.all(),
        # CalendarEvent
        'calendar_items': CalendarEvent.objects.filter(start__gte=timezone.now()),
        # Resources
        'resources': InfoResource.objects.all(),
        # Members.
        'all_profiles': Me.objects.all(),
    })
