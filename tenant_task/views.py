from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from tenant_intake.decorators import tenant_intake_required
from foundation_config.decorators import foundation_config_required
from tenant_profile.decorators import tenant_profile_required
from foundation_public import constants
from foundation_tenant.models.me import TenantMe
from foundation_tenant.forms.tagform import TagForm
from foundation_tenant.forms.intakeform import IntakeForm
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.intake import Intake


@login_required(login_url='/en/login')
@foundation_config_required
@tenant_intake_required
@tenant_profile_required
def tasks_list_page(request):
    return render(request, 'tenant_task/list/view.html',{
        'page': 'tasks',
    })


@login_required(login_url='/en/login')
@foundation_config_required
@tenant_intake_required
@tenant_profile_required
def intake_list_page(request):
    intakes = Intake.objects.all()
    return render(request, 'tenant_task/intake/list_view.html',{
        'page': 'tasks',
        'intakes': intakes,
    })