from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from foundation_public.decorators import group_required
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.entrepreneurnote import EntrepreneurNote
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_configuration_required
@tenant_profile_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
def entrepreneur_master_page(request, id):
    me = get_object_or_404(TenantMe, pk=int(id))
    return render(request, 'tenant_note/master/view.html',{
        'page': 'note',
        'me': me,
    })


@login_required(login_url='/en/login')
@tenant_configuration_required
@tenant_profile_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
def entrepreneur_details_page(request, me_id, note_id):
    me = get_object_or_404(TenantMe, pk=int(me_id))
    return render(request, 'tenant_note/details/view.html',{
        'page': 'note',
        'me': me,
    })
