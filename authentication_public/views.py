from django.core.signing import Signer
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import get_language
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from foundation_public import constants


def public_registration_page(request):
    return render(request, 'authentication_public/register_view.html',{})


def public_activation_required_page(request):
    return render(request, 'authentication_public/activation_required_view.html',{})


def public_activate_page(request, signed_value):
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

    return render(request, 'authentication_public/activate_view.html',{
        'user': user,
    })
