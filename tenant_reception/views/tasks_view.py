from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from foundation_tenant.forms.tagform import TagForm
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.note import Note
from foundation_tenant.models.task import Task
from smegurus import constants


@login_required(login_url='/en/login')
def reception_tasks_master_page(request):
    tasks = Task.objects.filter(assignee=request.tenant_me)
    return render(request, 'tenant_reception/task/master/view.html',{
        'page': 'reception-tasks-master',
        'tasks': tasks,
        'constants': constants,
    })


@login_required(login_url='/en/login')
def task_details_page(request, id):
    task = get_object_or_404(Task, pk=int(id))
    template_path = 'tenant_reception/task/details/view.html'
    return render(request, template_path, {
        # Required.
        'page': 'reception-tasks-details',
        'task': task,
        'constants': constants,
        # Tags.
        'tags': Tag.objects.all(),
        # Members.
        'entrepreneurs': TenantMe.objects.filter(owner__groups__id=constants.ENTREPRENEUR_GROUP_ID),
        'mentors': TenantMe.objects.filter(owner__groups__id=constants.MENTOR_GROUP_ID),
        'advisors': TenantMe.objects.filter(owner__groups__id=constants.ADVISOR_GROUP_ID),
        'managers': TenantMe.objects.filter(owner__groups__id=constants.ORGANIZATION_MANAGER_GROUP_ID),
        'admins': TenantMe.objects.filter(owner__groups__id=constants.ORGANIZATION_ADMIN_GROUP_ID),
    })
