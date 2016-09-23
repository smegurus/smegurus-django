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
from foundation_tenant.models.inforesource import InfoResource
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
# @condition(last_modified_func=my_last_modified_func)
def resource_page(request):
    return render(request, 'tenant_resource/master/view.html',{
        'page': 'resource',
        'inforesources': InfoResource.objects.all(),
        'constants': constants,
    })


@login_required(login_url='/en/login')
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
# @condition(last_modified_func=my_last_modified_func)
def resource_create_page(request):
    return render(request, 'tenant_resource/create/view.html',{
        'page': 'resource',
        'type_of': int_or_none(request.GET.get('type_of')),
        'constants': constants
    })


@login_required(login_url='/en/login')
@tenant_reception_required
@tenant_intake_required
@tenant_configuration_required
@tenant_profile_required
# @condition(last_modified_func=my_last_modified_func)
def resource_edit_details_page(request, id):
    inforesource = get_object_or_404(InfoResource, id=int_or_none(id))
    return render(request, 'tenant_resource/details/edit/view.html',{
        'page': 'resource',
        'constants': constants,
        'inforesource': inforesource
    })
