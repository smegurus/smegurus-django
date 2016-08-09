from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required


@login_required(login_url='/en/login')
@tenant_configuration_required
def reward_page(request):
    return render(request, 'tenant_reward/view.html',{
        'page': 'reward',
    })
