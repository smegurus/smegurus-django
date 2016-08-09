from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from foundation_config.decorators import foundation_config_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.intake import Intake
from smegurus import constants


@login_required(login_url='/en/login')
@foundation_config_required
@tenant_profile_required
def master_page(request):
    intakes = Intake.objects.filter(status=constants.APPROVED_STATUS)
    return render(request, 'tenant_customer/master/view.html',{
        'page': 'client',
        'intakes': intakes,
    })


@login_required(login_url='/en/login')
@foundation_config_required
@tenant_profile_required
def details_page(request, id):
    customer = get_object_or_404(TenantMe, pk=id)
    return render(request, 'tenant_customer/details/view.html',{
        'page': 'client',
        'customer': customer,
    })
