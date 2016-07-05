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
from smegurus.settings import env_var
from foundation_public import constants
from foundation_public.models.organization import PublicOrganization
from foundation_public.constants import *

def user_registration_page(request):
    return render(request, 'foundation_auth/user_register_view.html',{})


def user_activation_required_page(request):
    return render(request, 'foundation_auth/user_activation_required_view.html',{})


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
        return HttpResponseBadRequest("Failed activating this account.")

    # Get the user account and activate it.
    user = get_object_or_404(User, pk=value)
    user.is_active = True
    user.save()

    # Get the domain URL.
    org = PublicOrganization.objects.get(users__id=user.id)
    group = Group.objects.get(id=ENTREPRENEUR_GROUP_ID)
    login_url = resolve('foundation_auth_user_login')
    if group in user.groups.all():
        login_url = 'https://' if request.is_secure() else 'http://'
        login_url += str(org.schema_name) + '.'
        login_url += get_current_site(request).domain
        login_url += reverse('foundation_auth_user_login')

    return render(request, 'foundation_auth/user_activate_view.html',{
        'user': user,
        'login_url': login_url,
    })


def user_login_page(request):
    return render(request, 'foundation_auth/user_login_view.html',{})


@login_required(login_url='/en/login')
def user_launchpad_page(request):
    """
    Function will either redirect the User to the specific tenanted
    dashboard page or function will load the User to the Organization
    registration page.

    DEVELOPER NOTES:
    - Organization-User relationship is one to one.
    """
    if request.tenant.schema_name == 'public':
        return HttpResponseRedirect(reverse('foundation_auth_org_registration'))

    # Fetch the organization that this User belongs to.
    # Note: This only works because the assumption is there is One-to-One
    #       relationship between Organization and Users.
    org = get_object_or_404(PublicOrganization, users__id=request.user.id)
    # Generate our new URL.
    url = 'https://' if request.is_secure() else 'http://'
    url += str(org.schema_name) + '.'
    url += get_current_site(request).domain
    url += reverse('tenant_dashboard')
    return HttpResponseRedirect(url)  # Go to our new URL.


@login_required(login_url='/en/login')
def organization_registration_page(request):
    """
    Function provides the UI for a new User to create a new Organization to own.
    """
    org_membership_count = PublicOrganization.objects.filter(owner_id=request.user.id).count()
    if org_membership_count >= 1:
        return HttpResponseBadRequest(_("User cannot own any organization when registering a new organization."))
    else:
        return render(request, 'foundation_auth/organization_register_view.html',{})


@login_required(login_url='/en/login')
def organization_successful_registration(request):
    org = get_object_or_404(PublicOrganization, owner_id=request.user.id)

    # Generate our new URL.
    url = 'https://' if request.is_secure() else 'http://'
    url += str(org.schema_name) + '.'
    url += get_current_site(request).domain
    url += reverse('foundation_auth_user_login')

    return render(request, 'foundation_auth/organization_success_register_view.html',{
        'tenant_login_url': url
    })
