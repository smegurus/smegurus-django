from django.core.signing import Signer
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from foundation_public import constants
from foundation_public.models.organization import PublicOrganization


def public_user_registration_page(request):
    return render(request, 'authentication_public/user_register_view.html',{})


def public_user_activation_required_page(request):
    return render(request, 'authentication_public/user_activation_required_view.html',{})


def public_user_activate_page(request, signed_value):
    """
    Function will decode the 'signed_value' parameter and extract the User
    object from this value then set the User account to be active in our
    system.

    DEVELOPERS NOTE:
        - Users who get activated in this function will become assigned a
          'Organization Administrator'.
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

    # Attach group membership to 'Organization Administrator'.
    org_admin_group = get_object_or_404(Group, pk=constants.ORGANIZATION_ADMIN_GROUP_ID)
    user.groups.add(org_admin_group)

    return render(request, 'authentication_public/user_activate_view.html',{
        'user': user,
    })


def public_user_login_page(request):
    return render(request, 'authentication_public/user_login_view.html',{})


@login_required(login_url='/en/login')
def public_user_launchpad_page(request):
    """
    Function will either redirect the User to the specific tenanted
    dashboard page or function will load the User to the Organization
    registration page.
    """
    try:
        PublicOrganization.objects.get(owner_id=request.user.id)
        return HttpResponseRedirect('/en/dashboard') # TODO: replace with 'resolve()'.
    except PublicOrganization.DoesNotExist:
        return HttpResponseRedirect(reverse('public_org_registration'))


def public_org_registration_page(request):
    return render(request, 'authentication_public/org_register_view.html',{})
