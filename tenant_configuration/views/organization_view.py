import pytz
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework import status
from foundation_public.forms.userform import UserForm
from foundation_public.forms.loginform import LoginForm
from foundation_public.forms.organizationform import PublicOrganizationForm
from foundation_public.forms.postaladdressform import PublicPostalAddressForm
from foundation_public.models.organization import PublicOrganization
from foundation_public.decorators import group_required
from foundation_tenant.forms.businessideaform import BusinessIdeaForm
from foundation_tenant.forms.tellusyourneedform import TellUsYourNeedForm
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.businessidea import BusinessIdea
from foundation_tenant.models.tellusyourneed import TellUsYourNeed
from foundation_tenant.models.tag import Tag
from foundation_public.models.postaladdress import PublicPostalAddress
from smegurus import constants


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_one_page(request):
    return render(request, 'tenant_configuration/organization/1/view.html',{
        'org_form': PublicOrganizationForm(request.tenant),
    })


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_two_page(request):
    return render(request, 'tenant_configuration/organization/2/view.html',{})


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_three_page(request):
    return render(request, 'tenant_configuration/organization/3/view.html',{
        'tags': Tag.objects.all(),
    })


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_four_page(request):
    return render(request, 'tenant_configuration/organization/4/view.html',{})


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_five_page(request):
    return render(request, 'tenant_configuration/organization/5/view.html',{})


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_six_page(request):
    return render(request, 'tenant_configuration/organization/6/view.html',{})


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_seven_page(request):
    return render(request, 'tenant_configuration/organization/7/view.html',{})


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_eight_page(request):
    return render(request, 'tenant_configuration/organization/8/view.html',{
        'timezones': pytz.common_timezones
    })


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_nine_page(request):
    return render(request, 'tenant_configuration/organization/9/view.html',{})


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_ten_page(request):
    return render(request, 'tenant_configuration/organization/10/view.html',{})
