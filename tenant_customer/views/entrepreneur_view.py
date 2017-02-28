from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve, reverse
from django.utils.translation import get_language
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from foundation_public.decorators import group_required
from foundation_public.utils import random_text
from foundation_public.models.organization import PublicOrganization
from foundation_tenant.utils import int_or_none
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.contactpoint import ContactPoint
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.forms.postaladdressform import PostalAddressForm
from foundation_tenant.models.base.countryoption import CountryOption
from foundation_tenant.models.base.provinceoption import ProvinceOption
from foundation_tenant.models.base.naicsoption import NAICSOption
from smegurus import constants


@login_required(login_url='/en/login')
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def master_page(request):
    intakes = Intake.objects.filter(status=constants.APPROVED_STATUS)
    return render(request, 'tenant_customer/entrepreneur/master/view.html',{
        'page': 'client-entrepreneur',
        'intakes': intakes,
    })


@login_required(login_url='/en/login')
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def details_page(request, id):
    me = get_object_or_404(Me, pk=id)
    return render(request, 'tenant_customer/entrepreneur/details/view.html',{
        'page': 'client-entrepreneur',
        'me': me,
    })


@login_required(login_url='/en/login')
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def create_page(request):
    """Function will create a new Entrepreneur and redirect to the page of updating data."""
    schema_name = request.tenant.schema_name

    # Connection needs first to be at the public schema, as this is where
    # the tenant metadata is stored.
    from django.db import connection
    connection.set_schema_to_public() # Switch to Public.

    random_password = random_text(8)
    user = User.objects.create_user(
        username=random_text(30),
        email=random_text(100) + "@" + random_text(100) + ".com",
        password=random_password
    )
    entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
    user.groups.add(entrepreneur_group)

    # Attach our new User into our Organization.
    request.tenant.users.add(user)
    request.tenant.save()

    # Connection will set it back to our tenant.
    connection.set_schema(schema_name, True) # Switch back to Tenant.

    address = PostalAddress.objects.create(
        owner=user,
        name='User #' + str(user.id) + ' Address',
    )
    contact_point = ContactPoint.objects.create(
        owner=user,
        name='User #' + str(user.id) + ' Contact Point',
    )
    me = Me.objects.create(
        owner=user,
        address=address,
        contact_point=contact_point,
        is_in_intake=True,
        is_setup=True,
        temporary_password=random_password,
        managed_by=request.tenant_me
    )
    Intake.objects.create(
        me=me,
        status=constants.CREATED_STATUS,
    )
    url = reverse('tenant_customer_entrepreneur_create_step_1', args=[me.id,])
    return HttpResponseRedirect(url)


@login_required(login_url='/en/login')
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def create_step_one_page(request, pk):
    # Render our View.
    return render(request, 'tenant_customer/entrepreneur/create/1/view.html',{
        'page': 'client-entrepreneur',
        'me': get_object_or_404(Me, pk=pk)
    })


@login_required(login_url='/en/login')
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def create_step_two_page(request, pk):
    me = get_object_or_404(Me, pk=pk)

    # Fetch all the provinces for this Address.
    provinces = [] if not me.address.country else ProvinceOption.objects.filter(country=me.address.country)

    # Render our View.
    return render(request, 'tenant_customer/entrepreneur/create/2/view.html',{
        'page': 'client-entrepreneur',
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
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def create_step_three_page(request, pk):
    me = get_object_or_404(Me, pk=pk)
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
    return render(request, 'tenant_customer/entrepreneur/create/3/view.html',{
        'page': 'client-entrepreneur',
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
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def update_page(request, pk):
    me = get_object_or_404(Me, pk=pk)
    intake = get_object_or_404(Intake, me=me)

    # Fetch all the provinces for this Address.
    provinces = [] if not me.address.country else ProvinceOption.objects.filter(country=me.address.country)

    # Render our View.
    return render(request, 'tenant_customer/entrepreneur/update/view.html',{
        'page': 'client-entrepreneur',
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
