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
from foundation_public.forms.userform import UserForm
from foundation_public.forms.loginform import LoginForm
from foundation_public.models.organization import PublicOrganization
from foundation_public import constants
from smegurus.settings import env_var


def user_registration_page(request):
    return render(request, 'foundation_auth/user_register_view.html',{
        'form': UserForm(),
    })


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
    try:
        org = PublicOrganization.objects.get(users__id=user.id)
        group = Group.objects.get(id=ENTREPRENEUR_GROUP_ID)
        login_url = org.reverse(request, 'foundation_auth_user_login')
        if group in user.groups.all():
            login_url = org.reverse(request, 'foundation_auth_user_login')
    except PublicOrganization.DoesNotExist:
        login_url = reverse('foundation_auth_user_login')

    return render(request, 'foundation_auth/user_activate_view.html',{
        'user': user,
        'login_url': login_url,
    })


def user_login_page(request):
    return render(request, 'foundation_auth/user_login_view.html',{
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
        organization = PublicOrganization.objects.get(users__id=request.user.id)
        url = organization.reverse(request, 'tenant_dashboard')
        return HttpResponseRedirect(url)  # Go to our new URL.
    except PublicOrganization.DoesNotExist:
        return HttpResponseRedirect(reverse('foundation_auth_org_registration'))


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
    organization = get_object_or_404(PublicOrganization, owner_id=request.user.id)
    return render(request, 'foundation_auth/organization_success_register_view.html',{
        'organization': organization
    })
