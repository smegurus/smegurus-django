from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.views.decorators.http import condition
from rest_framework.authtoken.models import Token
from foundation_tenant.utils import my_last_modified_func
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required


@login_required(login_url='/en/login')
@tenant_configuration_required
@condition(last_modified_func=my_last_modified_func)
def resource_page(request):
    # print("TENANT", request.tenant.schema_name)
    # print("USER", request.token)
    return render(request, 'tenant_resource/view.html',{
        'page': 'resource',
    })
