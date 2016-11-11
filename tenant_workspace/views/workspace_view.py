from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from foundation_tenant.utils import int_or_none
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.base.me import TenantMe
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_configuration_required
def create_page(request):
    return render(request, 'tenant_workspace/workspace/create/view.html',{
        'page': 'workspace',
        'mes': TenantMe.objects.filter(owner__groups__id=constants.ENTREPRENEUR_GROUP_ID)
    })


@login_required(login_url='/en/login')
@tenant_configuration_required
def master_page(request, workspace_id):
    workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    modules = Module.objects.filter(stage_num__lte=workspace.stage_num)
    documents = Document.objects.all()
    return render(request, 'tenant_workspace/workspace/master/view.html',{
        'page': 'workspace',
        'workspace': workspace,
        'modules': modules,
        'documents': documents,
        'mes': TenantMe.objects.all()
    })
