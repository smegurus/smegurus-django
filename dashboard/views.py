from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from foundation_config.decorators import foundation_config_required

@foundation_config_required
@login_required(login_url='/en/login')
def dashboard_page(request):
    # print("TENANT", request.tenant.schema_name)
    # print("USER", request.token)
    return render(request, 'dashboard/view.html',{

    })
