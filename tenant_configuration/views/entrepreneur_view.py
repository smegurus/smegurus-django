import pytz
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework import status
from foundation_public.decorators import group_required
from foundation_tenant.forms.tenantmeform import TenantMeForm
from smegurus import constants


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_one_page(request):
    return render(request, 'tenant_configuration/entrepreneur/1_view.html',{})


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_two_page(request):
    return render(request, 'tenant_configuration/entrepreneur/2_view.html',{
        'form': TenantMeForm(instance=request.tenant_me)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_three_page(request):
    return render(request, 'tenant_configuration/entrepreneur/3_view.html',{
        'form': TenantMeForm(instance=request.tenant_me)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_four_page(request):
    return render(request, 'tenant_configuration/entrepreneur/4_view.html',{
        'form': TenantMeForm(instance=request.tenant_me)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_five_page(request):
    return render(request, 'tenant_configuration/entrepreneur/5_view.html',{
        'form': TenantMeForm(instance=request.tenant_me)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_six_page(request):
    return render(request, 'tenant_configuration/entrepreneur/6_view.html',{
        'form': TenantMeForm(instance=request.tenant_me)
    })
