from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import condition
from foundation_public.decorators import group_required
from foundation_public.utils import latest_date_between
from tenant_intake.decorators import tenant_intake_has_completed_redirection_required
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.countryoption import CountryOption
from foundation_tenant.models.provinceoption import ProvinceOption
from foundation_tenant.models.cityoption import CityOption
from smegurus import constants


def entrepreneur_func(request):
    """
    Function will return the last_modified date for the intake object of
    the Entrepreneurs account.
    """
    try:
        intake, create = Intake.objects.get_or_create(me=request.tenant_me)
        return latest_date_between(intake.last_modified, request.tenant_me.address.last_modified)
    except Intake.DoesNotExist:
        return datetime.now()


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@condition(last_modified_func=entrepreneur_func)
@tenant_intake_has_completed_redirection_required
def intake_entr_round_one_step_one_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_1/1/view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@condition(last_modified_func=entrepreneur_func)
@tenant_intake_has_completed_redirection_required
def intake_entr_round_one_step_two_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_1/2/view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@condition(last_modified_func=entrepreneur_func)
@tenant_intake_has_completed_redirection_required
def intake_entr_round_one_step_three_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_1/3/view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@condition(last_modified_func=entrepreneur_func)
@tenant_intake_has_completed_redirection_required
def intake_entr_round_one_step_four_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_1/4/view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'countries': CountryOption.objects.all()
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@condition(last_modified_func=entrepreneur_func)
@tenant_intake_has_completed_redirection_required
def intake_entr_round_one_step_five_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_1/5/view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
# @condition(last_modified_func=entrepreneur_func)
@tenant_intake_has_completed_redirection_required
def intake_entr_round_two_step_one_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_2/1/view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
    })





@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
@condition(last_modified_func=entrepreneur_func)
def intake_round_one_finished_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_1/finished/view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })
