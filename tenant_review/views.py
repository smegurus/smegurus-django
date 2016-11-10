from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from foundation_public.decorators import group_required
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.utils import int_or_none
from foundation_tenant.models.bizmula.documenttype import DocumentType
from foundation_tenant.models.bizmula.question import Question
from foundation_tenant.models.bizmula.questionoption import QuestionOption
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.slide import Slide
from foundation_tenant.models.bizmula.exercise import Exercise
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer
from smegurus import constants


@login_required(login_url='/en/login')
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_configuration_required
def master_page(request):
    documents = Document.objects.filter(
        status=constants.DOCUMENT_PENDING_REVIEW_STATUS,
        workspace__mes__managed_by__id=request.tenant_me.id
    )
    return render(request, 'tenant_review/master/view.html',{
        'page': 'review',
        'documents': documents
    })


@login_required(login_url='/en/login')
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_configuration_required
def detail_page(request, document_id):
    return render(request, 'tenant_review/detail/view.html',{
        'page': 'review',
        'document': get_object_or_404(Document, pk=int_or_none(document_id))
    })
