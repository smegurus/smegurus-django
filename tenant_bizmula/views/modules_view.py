from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.views.decorators.http import condition
from rest_framework.authtoken.models import Token
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from foundation_tenant.utils import my_last_modified_func
from tenant_bizmula.models.lecture import Lecture
# from tenant_bizmula.models.slide import Slide


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def master_page(request):
    lectures = Lecture.objects.filter(stage_num__lte=request.tenant_me.stage_num)
    return render(request, 'tenant_bizmula/modules/master/view.html',{
        'page': 'bizmula-module',
        'lectures': lectures
    })