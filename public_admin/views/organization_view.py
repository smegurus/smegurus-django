from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from foundation_public.models.organization import PublicOrganization
from foundation_public.forms.userform import UserForm
from foundation_public.forms.loginform import LoginForm
from foundation_public.forms.organizationform import PublicOrganizationForm
from foundation_public.forms.postaladdressform import PublicPostalAddressForm
from foundation_public.forms.contactpointform import PublicContactPointForm
from foundation_public.models.postaladdress import PublicPostalAddress
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
def organization_initialization_page(request):
    return render(request, 'public_admin/organization/create/0/view.html',{
        'org_form': PublicOrganizationForm(),
    })


@staff_member_required
def organization_create_1_page(request, id):
    organization = get_object_or_404(PublicOrganization, pk=int(id))

    # Generate address.
    if organization.address == None:
        organization.address = PublicPostalAddress.objects.create(
            name='#' + str(id) + ' HQ Address'
        )
        organization.save()

    # Return our code.
    return render(request, 'public_admin/organization/create/1/view.html',{
        'organization': organization,
        'address_form': PublicPostalAddressForm(instance=organization.address),
    })


@staff_member_required
def organization_create_2_page(request, id):
    organization = get_object_or_404(PublicOrganization, pk=int(id))
    return render(request, 'public_admin/organization/create/1/view.html',{
        # 'org_form': PublicOrganizationForm(),
        # 'address_form': PublicPostalAddressForm(instance=organization.address),
        'contact_form': PublicContactPointForm(instance=organization.contact_point),
    })
