from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User, Group
from django.utils.translation import get_language
from django.db.models import Q
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from foundation_public.decorators import group_required
from foundation_public.utils import random_text
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.contactpoint import ContactPoint
from foundation_tenant.forms.postaladdressform import PostalAddressForm
from foundation_tenant.models.base.countryoption import CountryOption
from foundation_tenant.models.base.provinceoption import ProvinceOption
from smegurus import constants


@login_required(login_url='/en/login')
@group_required([
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
    team_members = Me.objects.filter(
        Q(owner__groups__id=constants.MENTOR_GROUP_ID) |
        Q(owner__groups__id=constants.ADVISOR_GROUP_ID) |
        Q(owner__groups__id=constants.ORGANIZATION_MANAGER_GROUP_ID) |
        Q(owner__groups__id=constants.ORGANIZATION_ADMIN_GROUP_ID)
    ).distinct('id')
    return render(request, 'tenant_team/master/view.html',{
        'page': 'team',
        'team_members': team_members,
    })


@login_required(login_url='/en/login')
@group_required([
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
    """Function will create a new emplee and redirect to the page of updating data."""
    country_id = 0
    # Connection needs first to be at the public schema, as this is where
    # the tenant metadata is stored.
    from django.db import connection
    connection.set_schema_to_public() # Switch to Public.

    # Fetch the data.
    country_id = int(request.tenant.address.country.id)
    region_id = int(request.tenant.address.region.id)
    locality = str(request.tenant.address.locality)
    postal_code = str(request.tenant.address.postal_code)
    street_number = str(request.tenant.address.street_number)
    suffix = str(request.tenant.address.suffix)
    street_name = str(request.tenant.address.street_name)
    suite_number = str(request.tenant.address.suite_number)
    address_line_2 = str(request.tenant.address.address_line_2)
    address_line_3 = str(request.tenant.address.address_line_3)
    telephone = str(request.tenant.contact_point.telephone)

    # Generate User.
    random_password = random_text(8)
    user = User.objects.create_user(
        username=random_text(30),
        email=random_text(100) + "@" + random_text(100) + ".com",
        password=random_password,
        is_active=True
    )

    # Attach our new User into our Organization.
    request.tenant.users.add(user)
    request.tenant.save()

    # Connection will set it back to our tenant.
    connection.set_schema(request.tenant.schema_name, True) # Switch back to Tenant.

    # Begin...
    address = PostalAddress.objects.create(
        owner=user,
        name='User #' + str(user.id) + ' Address',
        country_id=country_id,
        region_id=region_id,
        locality=locality,
        postal_code=postal_code,
        street_number=street_number,
        suffix=suffix,
        street_name=street_name,
        suite_number=suite_number,
        address_line_2=address_line_2,
        address_line_3=address_line_3,
    )
    contact_point = ContactPoint.objects.create(
        owner=user,
        name='User #' + str(user.id) + ' Contact Point',
        telephone=telephone,
    )
    me = Me.objects.create(
        owner=user,
        address=address,
        contact_point=contact_point,
        is_in_intake=True,
        is_setup=True,
        managed_by=request.tenant_me
    )
    url = reverse('tenant_team_update', args=[me.id,]) + "?pass="+random_password
    return HttpResponseRedirect(url)


@login_required(login_url='/en/login')
@group_required([
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
    # Fetch the user.
    me = get_object_or_404(Me, pk=pk)

    # Fetch all the provinces for this Address.
    provinces = [] if not me.address.country else ProvinceOption.objects.filter(country=me.address.country)

    # Render our View.
    return render(request, 'tenant_team/details/view.html',{
        'page': 'team',
        'me': me,
        'groups': Group.objects.all(),
        'address_form': PostalAddressForm(instance=me.address),
        'countries': CountryOption.objects.all(),
        'provinces': provinces,
        'address_fields': [
            'id_locality', 'id_postal_code', 'id_street_number', 'id_suffix',
            'id_street_name', 'id_suite_number', 'id_address_line_2',
            'id_address_line_3',
        ],
        'temporary_password': request.GET.get('pass'),
    })
