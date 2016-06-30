from django.core.signing import Signer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.utils.translation import get_language
from django.contrib.auth.models import User


def public_registration_page(request):
    return render(request, 'registration_public/register_view.html',{})


def public_activation_required_page(request):
    return render(request, 'registration_public/activation_required_view.html',{})


def public_activate_page(request, signed_value):
    """
    Function will decode the 'signed_value' parameter and extract the User
    object from this value then set the User account to be active in our
    system.
    """
    try:
        # Convert our signed value into a text.
        signer = Signer()
        value = signer.unsign(signed_value)

        # Get the user account and activate it.
        user = User.objects.get(id=value)
        user.is_active = True
        user.save()
    except Exception as e:
        user = None

    return render(request, 'registration_public/activate_view.html',{
        'user': user,
    })
