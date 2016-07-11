from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework import status
from foundation_public.models.organization import PublicOrganization
from foundation_public import constants


def config_org_step_one_page(request):
    return render(request, 'foundation_config/organization/1_view.html',{

    })


def config_org_step_two_page(request):
    return render(request, 'foundation_config/organization/2_view.html',{

    })


def config_org_step_three_page(request):
    return render(request, 'foundation_config/organization/3_view.html',{

    })

def config_org_step_four_page(request):
    return render(request, 'foundation_config/organization/4_view.html',{

    })


def config_org_step_five_page(request):
    return render(request, 'foundation_config/organization/5_view.html',{

    })


def config_org_step_six_page(request):
    return render(request, 'foundation_config/organization/6_view.html',{

    })


def config_org_step_seven_page(request):
    return render(request, 'foundation_config/organization/7_view.html',{

    })


def config_org_step_eight_page(request):
    return render(request, 'foundation_config/organization/8_view.html',{

    })
