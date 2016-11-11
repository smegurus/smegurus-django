from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from foundation_tenant.models.bizmula.workspace import Workspace


@login_required(login_url='/en/login')
def reception_dashboard_master_page(request):
    try:
        workspace = Workspace.objects.get(mes__id=request.tenant_me.id)
    except Exception as e:
        workspace = None
    return render(request, 'tenant_reception/dashboard/master/view.html',{
        'page': 'reception-dashboard-master',
        'workspace': workspace
    })
