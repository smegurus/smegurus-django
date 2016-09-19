from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from foundation_tenant.models.task import Task


@login_required(login_url='/en/login')
def reception_tasks_master_page(request):
    unified_tasks = []
    upload_tasks = Task.objects.filter(assignee=request.tenant_me)


    return render(request, 'tenant_reception/todo/master/view.html',{
        'page': 'reception-dashboard-master',
        'unified_tasks': unified_tasks
    })
