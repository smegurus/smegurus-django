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





@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
@condition(last_modified_func=my_last_modified_func)
def create_page(request):
    """Function will create a new Entrepreneur and redirect to the page of updating data."""
    random_password = random_text(8)
    user = User.objects.create_user(
        username=random_text(30),
        email=random_text(100) + "@" + random_text(100) + ".com",
        password=random_password
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
        temporary_password=random_password
    )
    Intake.objects.create(
        me=me,
        status=constants.CREATED_STATUS,
    )
    url = reverse('tenant_customer_create_step_1', args=[me.id,])
    return HttpResponseRedirect(url)


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def create_step_one_page(request, pk):
    # Render our View.
    return render(request, 'tenant_customer/create/1/view.html',{
        'page': 'client',
        'me': get_object_or_404(TenantMe, pk=pk)
    })


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def create_step_two_page(request, pk):
    me = get_object_or_404(TenantMe, pk=pk)

    # Fetch all the provinces for this Address.
    provinces = [] if not me.address.country else ProvinceOption.objects.filter(country=me.address.country)

    # Render our View.
    return render(request, 'tenant_customer/create/2/view.html',{
        'page': 'client',
        'me': me,
        'form': PostalAddressForm(instance=me.address),
        'countries': CountryOption.objects.all(),
        'provinces': provinces,
        'accepted_fields': [
            'id_locality', 'id_postal_code', 'id_street_number', 'id_suffix',
            'id_street_name', 'id_suite_number', 'id_address_line_2',
            'id_address_line_3',
        ]
    })


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def create_step_three_page(request, pk):
    me = get_object_or_404(TenantMe, pk=pk)
    intake = get_object_or_404(Intake, me=me)

    # Get the first depth.
    depth_one_results = NAICSOption.objects.filter(parent=None)

    # Get the second depth.
    depth_two_results = None
    if intake.naics_depth_two:
        depth_two_results = NAICSOption.objects.filter(parent=intake.naics_depth_two.parent)
    else:
        if intake.naics_depth_one:
            depth_two_results = NAICSOption.objects.filter(parent=intake.naics_depth_one)

    # Get the three depth.
    depth_three_results = None
    if intake.naics_depth_three:
        depth_three_results = NAICSOption.objects.filter(parent=intake.naics_depth_three.parent)
    else:
        if intake.naics_depth_two:
            depth_three_results = NAICSOption.objects.filter(parent=intake.naics_depth_two)

    # Get the four depth.
    depth_four_results = None
    if intake.naics_depth_four:
        depth_four_results = NAICSOption.objects.filter(parent=intake.naics_depth_four.parent)
    else:
        if intake.naics_depth_three:
            depth_four_results = NAICSOption.objects.filter(parent=intake.naics_depth_three)

    # Get the five depth.
    depth_five_results = None
    if intake.naics_depth_five:
        depth_five_results = NAICSOption.objects.filter(parent=intake.naics_depth_five.parent)
    else:
        if intake.naics_depth_four:
            depth_five_results = NAICSOption.objects.filter(parent=intake.naics_depth_four)

    # Render our View.
    return render(request, 'tenant_customer/create/3/view.html',{
        'page': 'client',
        'me': me,
        'form': IntakeForm(instance=intake),
        'constants': constants,
        'rejected_fields': [
            'id_naics_depth_one', 'id_naics_depth_two', 'id_naics_depth_three',
            'id_naics_depth_four', 'id_naics_depth_five',
        ],
        'intake': intake,
        'depth_one_results': depth_one_results,
        'depth_two_results': depth_two_results,
        'depth_three_results': depth_three_results,
        'depth_four_results': depth_four_results,
        'depth_five_results': depth_five_results
    })


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
        'constants': constants,
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
