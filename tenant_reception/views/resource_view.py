from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from foundation_tenant.utils import int_or_none
from foundation_tenant.models.base.inforesourcecategory import InfoResourceCategory
from foundation_tenant.models.base.inforesource import InfoResource
from smegurus import constants


@login_required(login_url='/en/login')
def category_master_page(request):
    return render(request, 'tenant_reception/resource/master/category/view.html',{
        'page': 'reception-resource-master',
        'categories': InfoResourceCategory.objects.all(),
    })


@login_required(login_url='/en/login')
def resource_master_page(request, category_id):
    category = get_object_or_404(InfoResourceCategory, id=int_or_none(category_id))
    return render(request, 'tenant_reception/resource/master/resource/view.html',{
        'page': 'reception-resource-master',
        'category': category,
        'inforesources': InfoResource.objects.filter(
            category=category,
            stage_num__lte=request.tenant_me.stage_num,
        )
    })


@login_required(login_url='/en/login')
def resource_details_page(request, category_id, resource_id):
    return render(request, 'tenant_reception/resource/details/view.html',{
        'page': 'reception-resource-details',
        'resource': get_object_or_404(InfoResource, id=int(resource_id)),
        'constants': constants,
    })
