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
from foundation_tenant.models.naicsoption import NAICSOption
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.governmentbenefitoption import GovernmentBenefitOption
from foundation_tenant.models.identifyoption import IdentifyOption
from foundation_tenant.models.countryoption import CountryOption
from foundation_tenant.models.provinceoption import ProvinceOption
from foundation_tenant.models.cityoption import CityOption
from smegurus import constants


# def entrepreneur_func(request):
#     """
#     Function will return the last_modified date for the intake object of
#     the Entrepreneurs account.
#     """
#     try:
#         intake, create = Intake.objects.get_or_create(me=request.tenant_me)
#         return latest_date_between(intake.last_modified, request.tenant_me.address.last_modified)
#     except Intake.DoesNotExist:
#         return datetime.now()


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
# @condition(last_modified_func=entrepreneur_func)
@tenant_reception_required
def resource_master_page(request):
    # intake, create = Intake.objects.get_or_create(me=request.tenant_me)
    return render(request, 'tenant_inforesource/master/view.html',{
        # 'intake': intake,
        # 'form': IntakeForm(instance=intake),
        # 'tags': Tag.objects.filter(is_program=True)
    })
