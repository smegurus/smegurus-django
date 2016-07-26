from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from rest_framework import status

from foundation_public.forms.userform import UserForm
from foundation_public.forms.loginform import LoginForm
from foundation_public.forms.organizationform import PublicOrganizationForm
from foundation_public.forms.postaladdressform import PublicPostalAddressForm
from foundation_public.models.organization import PublicOrganization
from foundation_public.decorators import group_required
from foundation_public import constants

from foundation_tenant.forms.tagform import TagForm
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.intake import Intake

from tenant_intake.decorators import tenant_intake_required, tenant_intake_has_completed_redirection_required
from tenant_profile.decorators import tenant_profile_required


@login_required(login_url='/en/login')
@tenant_profile_required
@tenant_intake_required
def check_page(request):
    """Function will return either True or False depending if it meets decorator criteria."""
    from django.http import JsonResponse
    return JsonResponse({
        'access-granted':True
    })


@login_required(login_url='/en/login')
@tenant_profile_required
@tenant_intake_has_completed_redirection_required
def has_completed_intake_page(request):
    """Function will return either True or False depending if it meets decorator criteria."""
    from django.http import JsonResponse
    return JsonResponse({
        'access-granted':True
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@tenant_intake_has_completed_redirection_required
def intake_entr_step_one_page(request):
    intake, create = Intake.objects.get_or_create(owner=request.user)
    return render(request, 'tenant_intake/entrepreneur/1_view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@tenant_intake_has_completed_redirection_required
def intake_entr_step_two_page(request):
    intake, create = Intake.objects.get_or_create(owner=request.user)
    return render(request, 'tenant_intake/entrepreneur/2_view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@tenant_intake_has_completed_redirection_required
def intake_entr_step_three_page(request):
    intake, create = Intake.objects.get_or_create(owner=request.user)
    return render(request, 'tenant_intake/entrepreneur/3_view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@tenant_intake_has_completed_redirection_required
def intake_entr_step_four_page(request):
    intake, create = Intake.objects.get_or_create(owner=request.user)
    return render(request, 'tenant_intake/entrepreneur/4_view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@tenant_intake_has_completed_redirection_required
def intake_entr_step_five_page(request):
    intake, create = Intake.objects.get_or_create(owner=request.user)
    return render(request, 'tenant_intake/entrepreneur/5_view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def intake_entr_step_six_page(request):
    intake, create = Intake.objects.get_or_create(owner=request.user)
    return render(request, 'tenant_intake/entrepreneur/6_view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })
