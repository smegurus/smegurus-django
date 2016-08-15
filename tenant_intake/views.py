from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from rest_framework import status

from foundation_public.decorators import group_required
from tenant_configuration.decorators import tenant_configuration_required
from smegurus import constants

from foundation_tenant.forms.tagform import TagForm
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.me import TenantMe

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
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/1_view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@tenant_intake_has_completed_redirection_required
def intake_entr_step_two_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/2_view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@tenant_intake_has_completed_redirection_required
def intake_entr_step_three_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/3_view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@tenant_intake_has_completed_redirection_required
def intake_entr_step_four_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/4_view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@tenant_intake_has_completed_redirection_required
def intake_entr_step_five_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/5_view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def intake_entr_step_six_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/6_view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def intake_finished_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/finished_view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
def intake_master_page(request):
    intakes = Intake.objects.filter(
        Q(status=constants.PENDING_REVIEW_STATUS) |
        Q(status=constants.IN_REVIEW_STATUS) |
        Q(status=constants.REJECTED_STATUS)
    )
    return render(request, 'tenant_intake/employee/master/view.html',{
        'page': 'intake',
        'intakes': intakes,
    })


@login_required(login_url='/en/login')
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
def intake_details_page(request, id):
    intake = get_object_or_404(Intake, pk=id)
    return render(request, 'tenant_intake/employee/details/view.html',{
        'page': 'intake',
        'intake': intake,
        'form': IntakeForm(instance=intake),
    })
