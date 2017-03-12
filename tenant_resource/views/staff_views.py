from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User, Group
from foundation_public.decorators import group_required
from rest_framework.authtoken.models import Token
from foundation_tenant.utils import int_or_none
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from foundation_tenant.decorators import tenant_required
from foundation_tenant.models.base.inforesourcecategory import InfoResourceCategory
from foundation_tenant.models.base.inforesource import InfoResource
from foundation_tenant.models.base.tag import Tag
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
def staff_launchpad_page(request):
    return render(request, 'tenant_resource/staff/launchpad/master/view.html',{
        'page': 'resource',
    })


@login_required(login_url='/en/login')
@tenant_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
def staff_category_master_page(request):
    return render(request, 'tenant_resource/staff/category/master/view.html',{
        'page': 'resource',
        'categories': InfoResourceCategory.objects.all(),
    })


@login_required(login_url='/en/login')
@tenant_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
def staff_category_details_page(request, category_id):
    category = get_object_or_404(InfoResourceCategory, id=int_or_none(category_id))
    return render(request, 'tenant_resource/staff/category/details/view.html',{
        'page': 'resource',
        'category': category,
        'inforesources': InfoResource.objects.filter(category=category)
    })


@login_required(login_url='/en/login')
@tenant_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
def staff_resource_details_edit_page(request, category_id, resource_id):
    curr_category = get_object_or_404(InfoResourceCategory, id=int_or_none(category_id))
    curr_resource = get_object_or_404(InfoResource, id=int_or_none(resource_id))
    return render(request, 'tenant_resource/staff/resource/details/edit/view.html',{
        'page': 'resource',
        'resource': curr_resource,
        'categories': InfoResourceCategory.objects.all(),
        'tags': Tag.objects.all()
    })


@login_required(login_url='/en/login')
@tenant_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
def staff_resource_details_info_page(request, category_id, resource_id):
    curr_category = get_object_or_404(InfoResourceCategory, id=int_or_none(category_id))
    curr_resource = get_object_or_404(InfoResource, id=int_or_none(resource_id))
    return render(request, 'tenant_resource/staff/resource/details/info/view.html',{
        'page': 'resource',
        'resource': curr_resource,
        'categories': InfoResourceCategory.objects.all(),
        'tags': Tag.objects.all()
    })


@login_required(login_url='/en/login')
@tenant_required
@group_required([
    constants.ADVISOR_GROUP_ID,
    constants.ORGANIZATION_MANAGER_GROUP_ID,
    constants.ORGANIZATION_ADMIN_GROUP_ID,
    constants.CLIENT_MANAGER_GROUP_ID,
    constants.SYSTEM_ADMIN_GROUP_ID,
])
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
def staff_resource_create_page(request):
    return render(request, 'tenant_resource/staff/resource/create/view.html',{
        'page': 'resource',
        'categories': InfoResourceCategory.objects.all(),
        'tags': Tag.objects.all()
    })
