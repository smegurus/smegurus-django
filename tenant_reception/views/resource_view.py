from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from foundation_tenant.models.inforesource import InfoResource
from smegurus import constants


@login_required(login_url='/en/login')
def reception_resource_master_page(request):
    return render(request, 'tenant_reception/resource/master/view.html',{
        'page': 'reception-resource-master',
        'resources': InfoResource.objects.all(),
        'constants': constants,
    })


@login_required(login_url='/en/login')
def reception_resource_details_page(request, id):
    return render(request, 'tenant_reception/resource/details/view.html',{
        'page': 'reception-resource-details',
        'resource': get_object_or_404(InfoResource, id=int(id)),
        'constants': constants,
    })
