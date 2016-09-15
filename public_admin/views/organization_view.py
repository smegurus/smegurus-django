from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from foundation_public.models.organization import PublicOrganization
from foundation_public.forms.userform import UserForm
from foundation_public.forms.loginform import LoginForm
from foundation_public.forms.organizationform import PublicOrganizationForm
from foundation_public.forms.postaladdressform import PublicPostalAddressForm
from foundation_public.forms.contactpointform import PublicContactPointForm
from foundation_public.models.countryoption import CountryOption
from foundation_public.models.provinceoption import ProvinceOption
from foundation_public.models.cityoption import CityOption
from smegurus import constants
from smegurus.settings import env_var


@staff_member_required
def organization_menu_page(request):
    return render(request, 'public_admin/organization/menu_view.html',{})


@staff_member_required
def organization_master_page(request):
    return render(request, 'public_admin/organization/master/view.html',{})


@staff_member_required
def organization_create_1_page(request):
    return render(request, 'public_admin/organization/create/1/view.html',{
        'org_form': PublicOrganizationForm(),
        'address_form': PublicPostalAddressForm(),
        'contact_form': PublicContactPointForm(),
        'countries': CountryOption.objects.all()
    })


@staff_member_required
def organization_create_2_page(request):
    return render(request, 'public_admin/organization/create/1/view.html',{
        'org_form': PublicOrganizationForm(),
        'address_form': PublicPostalAddressForm(),
        'contact_form': PublicContactPointForm(),
        'countries': CountryOption.objects.all()
    })
