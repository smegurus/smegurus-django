from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from foundation_public.decorators import group_required
from tenant_configuration.decorators import tenant_configuration_required
from tenant_intake.decorators import tenant_intake_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.decorators import tenant_required
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.countryoption import CountryOption
from foundation_tenant.models.base.provinceoption import ProvinceOption
from foundation_tenant.models.base.cityoption import CityOption
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
def pending_intake_master_page(request):
    intakes = Intake.objects.filter(
        Q(status=constants.PENDING_REVIEW_STATUS) |
        Q(status=constants.IN_REVIEW_STATUS)
    )
    return render(request, 'tenant_intake/employee/master/view.html',{
        'page': 'intake-pending',
        'intakes': intakes,
        'type': 'pending'
    })


@login_required(login_url='/en/login')
@tenant_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
def held_intake_master_page(request):
    intakes = Intake.objects.filter(
        Q(status=constants.REJECTED_STATUS) |
        Q(status=constants.IN_REVIEW_STATUS)
    )
    return render(request, 'tenant_intake/employee/master/view.html',{
        'page': 'intake-held',
        'intakes': intakes,
        'type': 'held'
    })


@login_required(login_url='/en/login')
@tenant_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
def pending_intake_details_page(request, id):
    intake = get_object_or_404(Intake, pk=id)
    advisors = Me.objects.filter(owner__groups__id=constants.ADVISOR_GROUP_ID)
    tags = Tag.objects.filter(is_program=True)
    return render(request, 'tenant_intake/employee/details/view.html',{
        'page': 'intake-pending',
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'advisors': advisors,
        'tags': tags,
        'type': 'pending'
    })


@login_required(login_url='/en/login')
@tenant_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_configuration_required
@tenant_intake_required
@tenant_profile_required
def held_intake_details_page(request, id):
    intake = get_object_or_404(Intake, pk=id)
    advisors = Me.objects.filter(owner__groups__id=constants.ADVISOR_GROUP_ID)
    tags = Tag.objects.filter(is_program=True)
    return render(request, 'tenant_intake/employee/details/view.html',{
        'page': 'intake-held',
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'advisors': advisors,
        'tags': tags,
        'type': 'held'
    })
