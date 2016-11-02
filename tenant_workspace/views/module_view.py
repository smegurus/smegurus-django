from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from foundation_tenant.utils import int_or_none
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.slide import Slide
from foundation_tenant.models.bizmula.exercise import Exercise


@login_required(login_url='/en/login')
@tenant_configuration_required
def start_master_page(request, workspace_id, module_id):
    workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    module = get_object_or_404(Module, pk=int_or_none(module_id))
    return render(request, 'tenant_workspace/module/master/start/view.html',{
        'page': 'workspace',
        'workspace': workspace,
        'module': module
    })


@login_required(login_url='/en/login')
@tenant_configuration_required
def finish_master_page(request, workspace_id, module_id):
    workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    module = get_object_or_404(Module, pk=int_or_none(module_id))
    return render(request, 'tenant_workspace/module/master/finish/view.html',{
        'page': 'workspace',
        'workspace': workspace,
        'module': module
    })


@login_required(login_url='/en/login')
@tenant_configuration_required
def detail_page(request, workspace_id, module_id, slide_id):
    workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    module = get_object_or_404(Module, pk=int_or_none(module_id))
    slide = get_object_or_404(Slide, pk=int_or_none(slide_id))
    return render(request, 'tenant_workspace/module/detail/view.html',{
        'page': 'workspace',
        'workspace': workspace,
        'module': module,
        'slide': slide
    })
