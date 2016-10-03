from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User, Group
from django.utils.translation import get_language
from django.views.decorators.http import condition
from django.db.models import Q
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from foundation_public.decorators import group_required
from foundation_public.utils import random_text
from foundation_tenant.utils import my_last_modified_func
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.forms.postaladdressform import PostalAddressForm
from foundation_tenant.models.countryoption import CountryOption
from foundation_tenant.models.provinceoption import ProvinceOption
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
# @condition(last_modified_func=my_last_modified_func)
def master_page(request):
    team_members = TenantMe.objects.filter(
        Q(owner__groups__id=constants.MENTOR_GROUP_ID) |
        Q(owner__groups__id=constants.ADVISOR_GROUP_ID) |
        Q(owner__groups__id=constants.ORGANIZATION_MANAGER_GROUP_ID) |
        Q(owner__groups__id=constants.ORGANIZATION_ADMIN_GROUP_ID)
    )
    return render(request, 'tenant_team/master/view.html',{
        'page': 'team',
        'team_members': team_members,
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
# @condition(last_modified_func=my_last_modified_func)
def create_page(request):
    """Function will create a new emplee and redirect to the page of updating data."""
    # Fetch the Group the employee will belong to
    try:
        group_id = int(request.GET.get('group_id'))
        group = Group.objects.get(id=group_id)
    except Exception as e:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden(str(e))

    random_password = random_text(8)
    user = User.objects.create_user(
        username=random_text(30),
        email=random_text(100) + "@" + random_text(100) + ".com",
        password=random_password
    )
    user.groups.add(group)
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
    url = reverse('tenant_team_update', args=[me.id,]) + "?pass="+random_password
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
# @condition(last_modified_func=my_last_modified_func)
def update_page(request, pk):
    # Fetch the user.
    me = get_object_or_404(TenantMe, pk=pk)

    # Fetch all the provinces for this Address.
    provinces = [] if not me.address.country else ProvinceOption.objects.filter(country=me.address.country)

    # Render our View.
    return render(request, 'tenant_team/details/view.html',{
        'page': 'team',
        'me': me,
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
