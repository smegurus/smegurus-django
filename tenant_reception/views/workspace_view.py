from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from foundation_tenant.utils import int_or_none
from foundation_tenant.models.bizmula.documenttype import DocumentType
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.slide import Slide
from foundation_tenant.models.bizmula.question import Question
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer
from smegurus import constants


@login_required(login_url='/en/login')
def workspace_master_page(request, workspace_id):
    module = get_object_or_404(Module, stage_num=constants.ME_ONBOARDING_STAGE_NUM)
    first_node = module.get_first_node()
    url = reverse('tenant_reception_workspace_detail', args=[workspace_id, first_node['id']])
    return HttpResponseRedirect(url)


@login_required(login_url='/en/login')
def workspace_detail_page(request, workspace_id, node_id=0):
    workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    module = get_object_or_404(Module, stage_num=constants.ME_ONBOARDING_STAGE_NUM)
    node_id = int_or_none(node_id)
    node = module.get_node(node_id)

    # Either load up a "Slide" or load up the "Exercise".
    if node['type'] == "slide":
        return render(request, 'tenant_reception/workspace/detail/slide_view.html',{
            'page': 'workspace',
            'workspace': workspace,
            'module': module,
            'slide': get_object_or_404(Slide, pk=int_or_none(node['id'])),
            "node": node,
        })
    elif node['type'] == "question":
        question = get_object_or_404(Question, pk=int_or_none(node['id']))
        document_type = get_object_or_404(DocumentType, pk=int_or_none(node['document_type']))
        document = Document.objects.get(
            workspace=workspace,
            document_type=document_type
        )
        answer, created = QuestionAnswer.objects.get_or_create(
            workspace=workspace,
            document=document,
            question=question
        )
        return render(request, 'tenant_reception/workspace/detail/question_view.html',{
            'page': 'workspace',
            'workspace': workspace,
            'module': module,
            'question': question,
            "answer": answer,
            "node": node
        })

    # Generate a 404 error if the node reached does not have a supported format.
    raise Http404(_("Unsupported node format detected."))
