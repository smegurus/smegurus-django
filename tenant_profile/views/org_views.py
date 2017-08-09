from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from foundation_tenant.decorators import tenant_required
from foundation_tenant.forms.postaladdressform import PostalAddressForm
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.countryoption import CountryOption
from foundation_tenant.models.base.provinceoption import ProvinceOption
from foundation_tenant.models.base.cityoption import CityOption
from foundation_tenant.models.base.postaladdress import PostalAddress


@login_required(login_url='/en/login')
@tenant_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def profile_settings_profile_page(request):
    return render(request, 'tenant_profile/org/settings/profile/view.html',{
        'page': 'profile'
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def profile_settings_address_page(request):
    return render(request, 'tenant_profile/org/settings/address/view.html',{
        'page': 'profile'
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def profile_settings_preferences_page(request):
    return render(request, 'tenant_profile/org/settings/preferences/view.html',{
        'page': 'profile'
    })

# program_tags_page
@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def profile_settings_program_tags_page(request):
    return render(request, 'tenant_profile/org/settings/program_tags/view.html',{
        'page': 'profile'
    })


# client_tags_page
@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def profile_settings_client_tags_page(request):
    return render(request, 'tenant_profile/org/settings/client_tags/view.html',{
        'page': 'profile'
    })


# perks_page
@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def profile_settings_perks_page(request):
    return render(request, 'tenant_profile/org/settings/perks/view.html',{
        'page': 'profile'
    })


# affiliate_links_page
@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def profile_settings_affiliate_links_page(request):
    return render(request, 'tenant_profile/org/settings/affiliate_links/view.html',{
        'page': 'profile'
    })

