from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.views.decorators.http import condition
from rest_framework.authtoken.models import Token
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from foundation_tenant.utils import my_last_modified_func
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.countryoption import CountryOption
from foundation_tenant.models.provinceoption import ProvinceOption
from foundation_tenant.models.cityoption import CityOption


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
@condition(last_modified_func=my_last_modified_func)
def profile_page(request):
    return render(request, 'tenant_profile/generic/view.html',{
        'page': 'profile',
    })


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
@condition(last_modified_func=my_last_modified_func)
def profile_settings_page(request):
    countries = CountryOption.objects.all()
    provinces = [] if not request.tenant_me.address.country else ProvinceOption.objects.filter(country=request.tenant_me.address.country)
    cities = [] if not request.tenant_me.address.region else CityOption.objects.filter(province=request.tenant_me.address.region)
    return render(request, 'tenant_profile/settings/view.html',{
        'page': 'profile',
        'countries': countries,
        'provinces': provinces,
        'cities': cities
    })


@login_required(login_url='/en/login')
@condition(last_modified_func=my_last_modified_func)
def locked_page(request):
    """Function will lock the User out of our system and will require a password authentication to be let back in."""
    request.tenant_me.is_locked=True
    request.tenant_me.save()
    return render(request, 'tenant_profile/locked/view.html',{
        'page': 'profile',
    })


@tenant_profile_required
@condition(last_modified_func=my_last_modified_func)
def tenant_profile_is_locked_page(request):
    from django.http import JsonResponse
    """Function will return either True or False depending if a subdomain exists or not."""
    return JsonResponse({
        'access-granted':True
    })
