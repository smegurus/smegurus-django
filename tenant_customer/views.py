import random
from datetime import datetime
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
from foundation_tenant.utils import my_last_modified_func
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.intake import Intake
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.forms.postaladdressform import PostalAddressForm
from foundation_public.models.countryoption import CountryOption
from foundation_public.models.provinceoption import ProvinceOption
from foundation_public.models.cityoption import CityOption
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
@condition(last_modified_func=my_last_modified_func)
def master_page(request):
    intakes = Intake.objects.filter(status=constants.APPROVED_STATUS)
    return render(request, 'tenant_customer/master/view.html',{
        'page': 'client',
        'intakes': intakes,
    })


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def details_page(request, id):
    me = get_object_or_404(TenantMe, pk=id)
    return render(request, 'tenant_customer/details/view.html',{
        'page': 'client',
        'me': me,
    })


def random_text(size):
    """Randomly generate text"""
    alphabet_and_numbers = 'abcdefghijklmnopqrstuvwqyz1234567890'
    return(''.join(random.choice(alphabet_and_numbers) for _ in range(size)))


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
@condition(last_modified_func=my_last_modified_func)
def create_page(request):
    """Function will create a new Entrepreneur and redirect to the page of updating data."""
    user = User.objects.create_user(
        username=random_text(30),
        email=random_text(100) + "@" + random_text(100) + ".com",
        password=random_text(128)
    )
    entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
    user.groups.add(entrepreneur_group)
    address = PostalAddress.objects.create(
        owner=user,
        name='User #' + str(user.id) + ' Address',
    )
    contact_point = ContactPoint.objects.create(
        owner=user,
        name='User #' + str(user.id) + ' Contact Point',
    )
    me = TenantMe.objects.create(
        owner=user,
        address=address,
        contact_point=contact_point,
        is_admitted=True,
        is_setup=True,
    )
    Intake.objects.create(
        me=me,
        status=constants.CREATED_STATUS,
    )
    return HttpResponseRedirect(reverse('tenant_customer_update', args=[me.id,]))


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def update_page(request, pk):
    me = get_object_or_404(TenantMe, pk=pk)
    intake = get_object_or_404(Intake, me=me)

    # Fetch all the provinces for this Address.
    provinces = [] if not me.address.country else ProvinceOption.objects.filter(country=me.address.country)

    # Render our View.
    return render(request, 'tenant_customer/update/view.html',{
        'page': 'client',
        'me': me,
        'intake_form': IntakeForm(instance=intake),
        'address_form': PostalAddressForm(instance=me.address),
        'countries': CountryOption.objects.all(),
        'provinces': provinces,
        'accepted_fields': [
            'id_country', 'id_province',
            'id_postal_code', 'id_street_number', 'id_suffix', 'id_street_name',
            'id_suite_number', 'id_address_line_2', 'id_address_line_3',
        ]
    })
