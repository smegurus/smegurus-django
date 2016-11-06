from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.authtoken.models import Token
from foundation_tenant.utils import int_or_none
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.slide import Slide
from foundation_tenant.models.bizmula.question import Question


@login_required(login_url='/en/login')
@tenant_configuration_required
def start_master_page(request, workspace_id, module_id):
    workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    module = get_object_or_404(Module, pk=int_or_none(module_id))

    # Render our template with our variables.
    return render(request, 'tenant_workspace/module/master/start/view.html',{
        'page': 'workspace',
        'workspace': workspace,
        'module': module,
        'next_node_id': 0
    })


@login_required(login_url='/en/login')
@tenant_configuration_required
def detail_page(request, workspace_id, module_id, node_id):
    workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    module = get_object_or_404(Module, pk=int_or_none(module_id))
    node_id = int_or_none(node_id)
    node = module.get_node_data(node_id)

    # Either load up a "Slide" or load up the "Exercise".
    if node['type'] == "slide":
        slide = get_object_or_404(Slide, pk=int_or_none(node['id']))
        return render(request, 'tenant_workspace/module/detail/slice_view.html',{
            'page': 'workspace',
            'workspace': workspace,
            'module': module,
            'slide': slide,
            "node": node,
        })

    if node['type'] == "question":
        question = get_object_or_404(Question, pk=int_or_none(node['id']))
        return render(request, 'tenant_workspace/module/detail/question_view.html',{
            'page': 'workspace',
            'workspace': workspace,
            'module': module,
            'question': question,
            "node": node
        })

    raise Http404("Unsupported node detected.")


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
