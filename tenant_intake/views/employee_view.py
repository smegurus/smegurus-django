from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from foundation_public.decorators import group_required
from tenant_configuration.decorators import tenant_configuration_required
from tenant_intake.decorators import tenant_intake_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.me import TenantMe
from foundation_tenant.models.base.countryoption import CountryOption
from foundation_tenant.models.base.provinceoption import ProvinceOption
from foundation_tenant.models.base.cityoption import CityOption
from smegurus import constants


@login_required(login_url='/en/login')
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
def intake_master_page(request):
    intakes = Intake.objects.filter(
        Q(status=constants.PENDING_REVIEW_STATUS) |
        Q(status=constants.IN_REVIEW_STATUS)
    )
    return render(request, 'tenant_intake/employee/master/view.html',{
        'page': 'intake',
        'intakes': intakes,
    })


@login_required(login_url='/en/login')
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
def intake_details_page(request, id):
    intake = get_object_or_404(Intake, pk=id)
    advisors = TenantMe.objects.filter(owner__groups__id=constants.ADVISOR_GROUP_ID)
    tags = Tag.objects.filter(is_program=True)
    return render(request, 'tenant_intake/employee/details/view.html',{
        'page': 'intake',
        'intake': intake,
        'form': IntakeForm(instance=intake),
        'advisors': advisors,
        'tags': tags
    })
