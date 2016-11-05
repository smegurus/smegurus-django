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
# @tenant_configuration_required
def client_master_page(request, workspace_id, exercise_id):
    print("OKAY!!!")
    print(workspace_id)
    # workspace = get_object_or_404(Workspace, pk=int_or_none(workspace_id))
    # exercise = get_object_or_404(Exercise, pk=int_or_none(exercise_id))
    return render(request, 'tenant_workspace_exercise/client/master/view.html',{
        'page': 'workspace',
        'workspace': "workspace",
        'exercise': "exercise",
    })


@login_required(login_url='/en/login')
# @tenant_configuration_required
def client_detail_page(request, workspace_id, exercise_id):

    return render(request, 'tenant_workspace_exercise/client/master/view.html',{
        'page': 'workspace',
        'workspace': 0,
        'module': 0,
        'slide': 0
    })
