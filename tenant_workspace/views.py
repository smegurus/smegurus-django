from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from foundation_tenant.utils import int_or_none
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.bizmula.workspace import Workspace


@login_required(login_url='/en/login')
@tenant_configuration_required
def create_page(request):
    return render(request, 'tenant_workspace/create/view.html',{
        'page': 'workspace',
    })


@login_required(login_url='/en/login')
@tenant_configuration_required
def modules_master_page(request, workspace_id):
    workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    return render(request, 'tenant_workspace/master/view.html',{
        'page': 'workspace',
        'workspace': workspace
    })
