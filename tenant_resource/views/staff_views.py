from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.views.decorators.http import condition
from rest_framework.authtoken.models import Token
from foundation_tenant.utils import my_last_modified_func
from foundation_tenant.utils import int_or_none
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from foundation_tenant.models.inforesourcecategory import InfoResourceCategory
from foundation_tenant.models.inforesource import InfoResource
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
# @condition(last_modified_func=my_last_modified_func)
def staff_launchpad_page(request):
    return render(request, 'tenant_resource/staff/launchpad/master/view.html',{
        'page': 'resource',
    })


@login_required(login_url='/en/login')
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
# @condition(last_modified_func=my_last_modified_func)
def staff_category_master_page(request):
    return render(request, 'tenant_resource/staff/category/master/view.html',{
        'page': 'resource',
        'categories': InfoResourceCategory.objects.all(),
    })


@login_required(login_url='/en/login')
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
# @condition(last_modified_func=my_last_modified_func)
def staff_category_details_page(request, category_id):
    category = get_object_or_404(InfoResourceCategory, id=int_or_none(category_id))
    return render(request, 'tenant_resource/staff/category/details/view.html',{
        'page': 'resource',
        'category': category,
        'inforesources': InfoResource.objects.filter(category=category)
    })


@login_required(login_url='/en/login')
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
# @condition(last_modified_func=my_last_modified_func)
def staff_resource_details_page(request, category_id, resource_id):
    category = get_object_or_404(InfoResourceCategory, id=int_or_none(category_id))
    return render(request, 'tenant_resource/staff/category/details/view.html',{
        'page': 'resource',
        'category': category,
        'inforesources': InfoResource.objects.filter(category=category)
    })


@login_required(login_url='/en/login')
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
# @condition(last_modified_func=my_last_modified_func)
def staff_resource_create_page(request):
    return render(request, 'tenant_resource/staff/resource/create/view.html',{
        'page': 'resource',
    })
