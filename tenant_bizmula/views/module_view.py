from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.views.decorators.http import condition
from rest_framework.authtoken.models import Token
from foundation_tenant.utils import int_or_none
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from tenant_bizmula.models.module import Module
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def master_page(request, stage_num):
    module = get_object_or_404(Module, stage_num=int_or_none(stage_num))
    return render(request, 'tenant_bizmula/lectures/master/view.html',{
        'page': 'bizmula-module',
        'module': module
    })


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def detail_page(request, stage_num, slide_id):
    module = get_object_or_404(Module, stage_num=int_or_none(stage_num))
    return render(request, 'tenant_bizmula/lectures/master/view.html',{
        'page': 'bizmula-module',
        'module': module
    })
