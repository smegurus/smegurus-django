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
    return render(request, 'tenant_profile/me/settings/profile/view.html',{
        'page': 'profile'
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def profile_settings_address_page(request):
    return render(request, 'tenant_profile/me/settings/address/view.html',{
        'page': 'profile'
    })


# program_tags_page


# client_tags_page


# perks_page


# affiliate_links_page
