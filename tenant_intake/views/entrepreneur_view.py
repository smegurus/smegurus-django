from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import condition
from django.db.models import Q
from django.core.urlresolvers import reverse
from foundation_public.decorators import group_required
from foundation_public.utils import latest_date_between
from tenant_reception.decorators import tenant_reception_required
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.models.base.naicsoption import NAICSOption
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.me import TenantMe
from foundation_tenant.models.base.governmentbenefitoption import GovernmentBenefitOption
from foundation_tenant.models.base.identifyoption import IdentifyOption
from foundation_tenant.models.base.countryoption import CountryOption
from foundation_tenant.models.base.provinceoption import ProvinceOption
from foundation_tenant.models.base.cityoption import CityOption
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
# @condition(last_modified_func=entrepreneur_func)
@tenant_reception_required
def intake_entr_round_one_step_one_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_1/1/view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
# @condition(last_modified_func=entrepreneur_func)
@tenant_reception_required
def intake_entr_round_one_step_two_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_1/2/view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
# @condition(last_modified_func=entrepreneur_func)
@tenant_reception_required
def intake_entr_round_one_step_three_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_1/3/view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'tags': Tag.objects.filter(is_program=True)
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
# @condition(last_modified_func=entrepreneur_func)
@tenant_reception_required
def intake_entr_round_one_step_four_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_1/4/view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'countries': CountryOption.objects.all()
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
# @condition(last_modified_func=entrepreneur_func)
@tenant_reception_required
def intake_entr_round_one_step_five_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_1/5/view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
# @condition(last_modified_func=entrepreneur_func)
@tenant_reception_required
def intake_entr_round_one_step_six_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_1/6/view.html',{
        'intake': intake,
        'form': IntakeForm(instance=intake),
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
# @condition(last_modified_func=entrepreneur_func)
@tenant_reception_required
def intake_entr_round_two_step_one_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_2/1/view.html',{
        'intake': intake,
        'benefits': GovernmentBenefitOption.objects.all(),
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
# @condition(last_modified_func=entrepreneur_func)
@tenant_reception_required
def intake_entr_round_two_step_two_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_2/2/view.html',{
        'intake': intake,
        'identities': IdentifyOption.objects.all()
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
# @condition(last_modified_func=entrepreneur_func)
@tenant_reception_required
def intake_entr_round_two_step_three_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_2/3/view.html',{
        'intake': intake,
        'identities': IdentifyOption.objects.all()
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
# @condition(last_modified_func=entrepreneur_func)
@tenant_reception_required
def intake_entr_round_two_step_four_page(request):
    # Fetch the Intake object.
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)

    # Get the first depth.
    depth_one_results = NAICSOption.objects.filter(parent=None)

    # Get the second depth.
    depth_two_results = None
    if intake.naics_depth_two:
        depth_two_results = NAICSOption.objects.filter(parent=intake.naics_depth_two.parent)
    else:
        if intake.naics_depth_one:
            depth_two_results = NAICSOption.objects.filter(parent=intake.naics_depth_one)

    # Get the three depth.
    depth_three_results = None
    if intake.naics_depth_three:
        depth_three_results = NAICSOption.objects.filter(parent=intake.naics_depth_three.parent)
    else:
        if intake.naics_depth_two:
            depth_three_results = NAICSOption.objects.filter(parent=intake.naics_depth_two)

    # Get the four depth.
    depth_four_results = None
    if intake.naics_depth_four:
        depth_four_results = NAICSOption.objects.filter(parent=intake.naics_depth_four.parent)
    else:
        if intake.naics_depth_three:
            depth_four_results = NAICSOption.objects.filter(parent=intake.naics_depth_three)

    # Get the five depth.
    depth_five_results = None
    if intake.naics_depth_five:
        depth_five_results = NAICSOption.objects.filter(parent=intake.naics_depth_five.parent)
    else:
        if intake.naics_depth_four:
            depth_five_results = NAICSOption.objects.filter(parent=intake.naics_depth_four)

    # Render the view.
    return render(request, 'tenant_intake/entrepreneur/round_2/4/view.html',{
        'intake': intake,
        'depth_one_results': depth_one_results,
        'depth_two_results': depth_two_results,
        'depth_three_results': depth_three_results,
        'depth_four_results': depth_four_results,
        'depth_five_results': depth_five_results
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
# @condition(last_modified_func=entrepreneur_func)
@tenant_reception_required
def intake_entr_round_two_step_five_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_2/5/view.html',{
        'intake': intake,
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
# @condition(last_modified_func=entrepreneur_func)
def intake_round_two_finished_page(request):
    intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_intake/entrepreneur/round_2/finished/view.html',{
        'intake': intake,
        'dashboard_url': reverse('tenant_reception')
    })
