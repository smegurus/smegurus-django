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
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def profile_page(request):
    return render(request, 'tenant_profile/me/generic/view.html',{
        'page': 'profile',
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def profile_settings_profile_page(request):
    return render(request, 'tenant_profile/me/settings/profile/view.html',{
        'page': 'profile'
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def profile_settings_address_page(request):
    address = request.tenant_me.address
    countries = CountryOption.objects.all()
    provinces = [] if not address.country else ProvinceOption.objects.filter(country=address.country)
    return render(request, 'tenant_profile/me/settings/address/view.html',{
        'page': 'profile',
        'countries': countries,
        'provinces': provinces,
        'address': address,
        'form': PostalAddressForm(instance=address),
        'accepted_fields': [
            'id_postal_code', 'id_street_number', 'id_suffix', 'id_street_name',
            'id_suite_number', 'id_address_line_2', 'id_address_line_3',
        ]
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def profile_settings_password_page(request):
    return render(request, 'tenant_profile/me/settings/password/view.html',{
        'page': 'profile'
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def profile_settings_notification_page(request):
    return render(request, 'tenant_profile/me/settings/notification/view.html',{
        'page': 'profile'
    })


@login_required(login_url='/en/login')
@tenant_required
def locked_page(request):
    """Function will lock the User out of our system and will require a password authentication to be let back in."""
    request.tenant_me.is_locked=True
    request.tenant_me.save()
    return render(request, 'tenant_profile/me/locked/view.html',{
        'page': 'profile',
    })


@tenant_profile_required
@tenant_required
def tenant_profile_is_locked_page(request):
    from django.http import JsonResponse
    """Function will return either True or False depending if a subdomain exists or not."""
    return JsonResponse({
        'access-granted':True
    })
