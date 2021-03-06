# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.authtoken.models import Token
from foundation_tenant.utils import int_or_none
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.decorators import tenant_required
from foundation_tenant.models.bizmula.documenttype import DocumentType
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.slide import Slide
from foundation_tenant.models.bizmula.question import Question
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer


@login_required(login_url='/en/login')
@tenant_required
@tenant_configuration_required
def start_master_page(request, workspace_id, module_id):
    workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    module = get_object_or_404(Module, pk=int_or_none(module_id))

    # Render our template with our variables.
    return render(request, 'tenant_workspace/module/master/start/view.html',{
        'page': str(workspace),
        'workspace': workspace,
        'module': module,
        'first_node': module.get_first_node()
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_configuration_required
def detail_page(request, workspace_id, module_id, node_id):
    workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    module = get_object_or_404(Module, pk=int_or_none(module_id))
    node_id = int_or_none(node_id)
    node = module.get_node(node_id)

    # Either load up a "Slide" or load up the "Question".
    if node['type'] == "slide":
        return render(request, 'tenant_workspace/module/detail/slice_view.html',{
            'page': str(workspace),
            'workspace': workspace,
            'module': module,
            'slide': get_object_or_404(Slide, pk=int_or_none(node['id'])),
            "node": node,
        })

    elif node['type'] == "question":
        question = get_object_or_404(Question, pk=int_or_none(node['id']))
        document_type = get_object_or_404(DocumentType, pk=int_or_none(node['document_type']))
        document, created = Document.objects.get_or_create(
            workspace=workspace,
            document_type=document_type,
            name=str(document_type)
        )
        answer, created = QuestionAnswer.objects.get_or_create(
            workspace=workspace,
            document=document,
            question=question
        )
        return render(request, 'tenant_workspace/module/detail/question_view.html',{
            'page': str(workspace),
            'workspace': workspace,
            'module': module,
            'question': question,
            "answer": answer,
            "node": node
        })

    # Generate a 404 error if the node reached does not have a supported format.
    raise Http404(_("Unsupported node format detected."))


@login_required(login_url='/en/login')
@tenant_required
@tenant_configuration_required
def submit_master_page(request, workspace_id, module_id, previous_node_id):
    """
    Function will generate the document which will be submitted for processing
    using the API.
    """
    # Fetch our associated models.
    workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    module = get_object_or_404(Module, pk=int_or_none(module_id))

    # Fetch the document type.
    document_type_id = module.get_document_type_id()
    document_type = DocumentType.objects.get(id=document_type_id)

    # Fetch the document associated with this Module.
    document, created = Document.objects.get_or_create(
        workspace=workspace,
        document_type=document_type,
        name=document_type.text
    )

    # Render the template.
    return render(request, 'tenant_workspace/module/master/submit/view.html',{
        'page': str(workspace),
        'workspace': workspace,
        'module': module,
        'last_node': module.get_last_node(),
        'document': document
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_configuration_required
def finish_master_page(request, workspace_id, module_id):
    # Fetch our associated models.
    workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    module = get_object_or_404(Module, pk=int_or_none(module_id))

    # Fetch the document associated with this Module.
    document_type_id = module.get_document_type_id()
    document = Document.objects.get(
        workspace=workspace,
        document_type_id=document_type_id
    )

    # Render the template.
    return render(request, 'tenant_workspace/module/master/finish/view.html',{
        'page': str(workspace),
        'workspace': workspace,
        'module': module,
        'last_node': module.get_last_node(),
        'document': document
    })
