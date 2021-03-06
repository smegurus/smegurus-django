from django.core.signing import Signer
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import get_language
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from foundation_public.models.organizationregistration import PublicOrganizationRegistration
from foundation_public.models.organization import PublicOrganization
from foundation_public.forms.userform import UserForm
from foundation_public.forms.loginform import LoginForm
from foundation_public.forms.organizationform import PublicOrganizationForm
from foundation_public.forms.postaladdressform import PublicPostalAddressForm
from foundation_public.models.countryoption import CountryOption
from foundation_public.models.provinceoption import ProvinceOption
from foundation_public.models.cityoption import CityOption
from smegurus import constants


def user_registration_page(request):
    return render(request, 'foundation_auth/user_registration/view.html',{
        'form': UserForm(),
    })


def user_activation_required_page(request):
    return render(request, 'foundation_auth/user_activation_required/view.html',{})


def user_activate_page(request, signed_value):
    """
    Function will decode the 'signed_value' parameter and extract the User
    object from this value then set the User account to be active in our
    system.
    """
    try:
        # Convert our signed value into a text.
        signer = Signer()
        value = signer.unsign(signed_value)
    except Exception as e:
        return HttpResponseBadRequest(_("Failed activating this account."))

    # Get the user account and activate it.
    user = get_object_or_404(User, pk=value)
    user.is_active = True
    user.save()

    # Get the domain URL.
    try:
        org = PublicOrganization.objects.get(users__id=user.id)
        group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        login_url = org.reverse('foundation_auth_user_login')
        if group in user.groups.all():
            login_url = org.reverse('foundation_auth_user_login')
    except PublicOrganization.DoesNotExist:
        login_url = reverse('foundation_auth_user_login')

    return render(request, 'foundation_auth/user_activation/view.html',{
        'user': user,
        'login_url': login_url,
    })


def user_login_page(request):
    return render(request, 'foundation_auth/login/view.html',{
        'form': LoginForm(),
    })


@login_required(login_url='/en/login')
def user_launchpad_page(request):
    """
    Function will either redirect the User to the specific tenanted
    dashboard page or function will load the User to the Organization
    registration page.

    DEVELOPER NOTES:
    - Organization-User relationship is one to one.
    """
    # First check to see if this User belongs to any Organizations and if
    # the User does then go to that Organizations "Dashboard".
    try:
        organization = PublicOrganization.objects.get(users__id=int(request.user.id))
        url = organization.reverse('tenant_dashboard')
        return HttpResponseRedirect(url)  # Go to our new URL.
    except PublicOrganization.DoesNotExist:
        return HttpResponseRedirect(reverse('foundation_auth_org_registration'))


@login_required(login_url='/en/login')
def organization_registration_page(request):
    """
    Function provides the UI for a new User to create a new Organization to own.
    """
    org_membership_count = PublicOrganizationRegistration.objects.filter(owner_id=request.user.id).count()
    if org_membership_count >= 1:
        return HttpResponseRedirect(reverse('foundation_auth_org_successful_registration'))
    else:
        return render(request, 'foundation_auth/org_registration/view.html',{
            'org_form': PublicOrganizationForm(),
            'address_form': PublicPostalAddressForm(),
            'countries': CountryOption.objects.all()
        })


@login_required(login_url='/en/login')
def organization_successful_registration_page(request):
    return render(request, 'foundation_auth/org_registration_success/view.html',{})


def password_reset_page(request):
    return render(request, 'foundation_auth/user_password_reset/view.html',{})


def password_change_page(request, signed_value):
    try:
        # Convert our signed value into a text.
        signer = Signer()
        value = signer.unsign(signed_value)
    except Exception as e:
        return HttpResponseBadRequest(_("Failed activating this account."))

    token, created = Token.objects.get_or_create(user_id=value)
    return render(request, 'foundation_auth/user_password_change/view.html',{
        'uid': value,
        'token': token,
    })


def password_reset_sent_page(request):
    return render(request, 'foundation_auth/user_password_sent_reset/view.html',{})
