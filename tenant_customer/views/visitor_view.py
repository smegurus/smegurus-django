from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve, reverse
from django.utils.translation import get_language
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.views.decorators.http import condition
from rest_framework.authtoken.models import Token
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from foundation_public.decorators import group_required
from foundation_public.utils import random_text
from foundation_tenant.utils import my_last_modified_func, int_or_none
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.intake import Intake
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.forms.postaladdressform import PostalAddressForm
from foundation_tenant.models.countryoption import CountryOption
from foundation_tenant.models.provinceoption import ProvinceOption
from foundation_tenant.models.naicsoption import NAICSOption
from smegurus import constants


@login_required(login_url='/en/login')
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def master_page(request):
    intakes = Intake.objects.filter(status=constants.APPROVED_STATUS)
    return render(request, 'tenant_customer/visitor/master/view.html',{
        'page': 'client-visitor',
        'visitors': TenantMe.objects.filter(
            stage_num=1,
            owner__groups__id=constants.ENTREPRENEUR_GROUP_ID
        ),
    })


@login_required(login_url='/en/login')
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def details_page(request, pk):
    me = get_object_or_404(TenantMe, pk=int(pk))
    intake = get_object_or_404(Intake, me=me)
    return render(request, 'tenant_customer/visitor/detail/view.html',{
        'page': 'client-visitor',
        'intake': intake,
        'form': IntakeForm(instance=intake),
    })