from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.views.decorators.http import condition
from django.db.models import Q
from rest_framework.authtoken.models import Token
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from foundation_public.decorators import group_required
from foundation_tenant.utils import my_last_modified_func
from foundation_tenant.models.me import TenantMe
from smegurus import constants


@login_required(login_url='/en/login')
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def master_page(request):
    team_members = TenantMe.objects.filter(
        Q(owner__groups__id=constants.MENTOR_GROUP_ID) |
        Q(owner__groups__id=constants.ADVISOR_GROUP_ID) |
        Q(owner__groups__id=constants.ORGANIZATION_MANAGER_GROUP_ID) |
        Q(owner__groups__id=constants.ORGANIZATION_ADMIN_GROUP_ID)
    )
    return render(request, 'tenant_team/master/view.html',{
        'page': 'team',
        'team_members': team_members,
    })
