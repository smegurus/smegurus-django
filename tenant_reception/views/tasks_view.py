from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from foundation_tenant.models.uploadtask import UploadTask
from foundation_tenant.models.learningtask import LearningTask


@login_required(login_url='/en/login')
def reception_tasks_master_page(request):
    unified_tasks = []
    upload_tasks = UploadTask.objects.filter(assignee=request.tenant_me)
    learning_tasks = LearningTask.objects.filter(assignee=request.tenant_me)
    for i in upload_tasks.all():
        unified_tasks.append(i)
    for i in learning_tasks.all():
        unified_tasks.append(i)
    print(unified_tasks)

    return render(request, 'tenant_reception/todo/master/view.html',{
        'page': 'reception-dashboard-master',
        'unified_tasks': unified_tasks
    })
