from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework import status
from foundation_public.models.organization import PublicOrganization
from foundation_public.decorators import group_required
from foundation_public import constants


@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_one_page(request):
    return render(request, 'foundation_config/organization/1_view.html',{

    })


@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_two_page(request):
    return render(request, 'foundation_config/organization/2_view.html',{

    })


@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_three_page(request):
    return render(request, 'foundation_config/organization/3_view.html',{

    })


@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_four_page(request):
    return render(request, 'foundation_config/organization/4_view.html',{

    })


@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_five_page(request):
    return render(request, 'foundation_config/organization/5_view.html',{

    })


@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_six_page(request):
    return render(request, 'foundation_config/organization/6_view.html',{

    })


@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_seven_page(request):
    return render(request, 'foundation_config/organization/7_view.html',{

    })


@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_eight_page(request):
    return render(request, 'foundation_config/organization/8_view.html',{

    })


@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_one_page(request):
    return render(request, 'foundation_config/entrepreneur/1_view.html',{

    })


@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_two_page(request):
    return render(request, 'foundation_config/entrepreneur/2_view.html',{

    })


@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_three_page(request):
    return render(request, 'foundation_config/entrepreneur/3_view.html',{

    })


@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_four_page(request):
    return render(request, 'foundation_config/entrepreneur/4_view.html',{

    })
