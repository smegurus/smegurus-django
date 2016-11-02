import pytz
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework import status
from foundation_public.forms.organizationform import PublicOrganizationForm
from foundation_public.forms.postaladdressform import PublicPostalAddressForm
from foundation_public.models.organization import PublicOrganization
from foundation_public.decorators import group_required
from foundation_tenant.forms.businessideaform import BusinessIdeaForm
from foundation_tenant.forms.tellusyourneedform import TellUsYourNeedForm
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.businessidea import BusinessIdea
from foundation_tenant.models.base.tellusyourneed import TellUsYourNeed
from foundation_tenant.models.base.tag import Tag
from foundation_public.models.postaladdress import PublicPostalAddress
from foundation_public.models.countryoption import CountryOption
from foundation_public.models.provinceoption import ProvinceOption
from foundation_public.models.cityoption import CityOption
from smegurus import constants
from smegurus.settings import env_var


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_one_page(request):
    # Connection needs first to be at the public schema, as this is where
    # the tenant metadata is stored.
    from django.db import connection
    connection.set_schema_to_public()
        
    # Fetch all the provinces for this Address.
    provinces = [] if not request.tenant.address.country else ProvinceOption.objects.filter(country=request.tenant.address.country)

    # Connection will turn back to the Tenant from the Public b/c of the
    # "django-tenants" middleware we are using.
    return render(request, 'tenant_configuration/organization/1/view.html',{
        'countries': CountryOption.objects.all(),
        'provinces': provinces,
        'form': PublicPostalAddressForm(instance=request.tenant.address),
        'accepted_fields': [
            'id_postal_code', 'id_street_number', 'id_suffix', 'id_street_name',
            'id_suite_number', 'id_address_line_2', 'id_address_line_3',
        ],
        'constants': constants
    })


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_two_page(request):
    return render(request, 'tenant_configuration/organization/2/view.html',{
        'org_form': PublicOrganizationForm(request.tenant),
    })


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_three_page(request):
    return render(request, 'tenant_configuration/organization/3/view.html',{})


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_four_page(request):
    return render(request, 'tenant_configuration/organization/4/view.html',{
        'tags': Tag.objects.all(),
    })


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_five_page(request):
    return render(request, 'tenant_configuration/organization/5/view.html',{
        'timezones': pytz.common_timezones
    })


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_six_page(request):
    return render(request, 'tenant_configuration/organization/6/view.html',{})


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_seven_page(request):
    return render(request, 'tenant_configuration/organization/7/view.html',{
        'form': PublicOrganizationForm(instance=request.tenant),
        'accepted_fields': [
            'id_how_many_served', 'id_how_discovered',
        ],
    })


@login_required(login_url='/en/login')
@group_required([constants.ORGANIZATION_ADMIN_GROUP_ID,])
def config_org_step_eight_page(request):
    return render(request, 'tenant_configuration/organization/8/view.html',{})
