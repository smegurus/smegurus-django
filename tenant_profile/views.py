from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from tenant_profile.decorators import tenant_profile_required


@login_required(login_url='/en/login')
@tenant_profile_required
def profile_page(request):
    return render(request, 'tenant_profile/profile_view.html',{
        'page': 'profile',
    })


@login_required(login_url='/en/login')
@tenant_profile_required
def profile_settings_page(request):
    return render(request, 'tenant_profile/profile_settings_view.html',{
        'page': 'profile',
    })


@login_required(login_url='/en/login')
def locked_page(request):
    """Function will lock the User out of our system and will require a password authentication to be let back in."""
    request.public_me.is_locked=True
    request.public_me.save()
    return render(request, 'tenant_profile/is_locked_view.html',{
        'page': 'profile',
    })


@tenant_profile_required
def tenant_profile_is_locked_page(request):
    from django.http import JsonResponse
    """Function will return either True or False depending if a subdomain exists or not."""
    return JsonResponse({
        'access-granted':True
    })
