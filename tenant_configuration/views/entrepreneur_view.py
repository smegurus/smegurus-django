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
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_one_page(request):
    return render(request, 'tenant_configuration/entrepreneur/1_view.html',{})


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_two_page(request):
    businessidea, create = BusinessIdea.objects.get_or_create(owner=request.user)
    return render(request, 'tenant_configuration/entrepreneur/2_view.html',{
        'businessidea': businessidea,
        'form': BusinessIdeaForm(instance=businessidea),
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_three_page(request):
    tellusyourneed, create = TellUsYourNeed.objects.get_or_create(owner=request.user)
    return render(request, 'tenant_configuration/entrepreneur/3_view.html',{
        'tellusyourneed': tellusyourneed,
        'form': TellUsYourNeedForm(instance=tellusyourneed),
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_four_page(request):
    return render(request, 'tenant_configuration/entrepreneur/4_view.html',{
        'tags': Tag.objects.all(),
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def config_entr_step_five_page(request):
    return render(request, 'tenant_configuration/entrepreneur/5_view.html',{})