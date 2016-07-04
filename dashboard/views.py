from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@login_required(login_url='/en/login')
def dashboard_page(request):
    print("TENANT", request.tenant.schema_name)
    print("USER", request.token)
    return render(request, 'dashboard/view.html',{

    })
