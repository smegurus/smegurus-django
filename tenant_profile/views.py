from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@login_required(login_url='/en/login')
def profile_page(request):
    return render(request, 'tenant_profile/profile_view.html',{
        'page': 'profile',
    })


@login_required(login_url='/en/login')
def profile_settings_page(request):
    return render(request, 'tenant_profile/profile_settings_view.html',{
        'page': 'profile',
    })
