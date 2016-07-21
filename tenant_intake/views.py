from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework import status

from foundation_public.forms.userform import UserForm
from foundation_public.forms.loginform import LoginForm
from foundation_public.forms.organizationform import PublicOrganizationForm
from foundation_public.forms.postaladdressform import PublicPostalAddressForm
from foundation_public.forms.meform import PublicMeForm
from foundation_public.models.organization import PublicOrganization
from foundation_public.decorators import group_required
from foundation_public import constants

from foundation_tenant.forms.businessideaform import BusinessIdeaForm
from foundation_tenant.forms.tellusyourneedform import TellUsYourNeedForm
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.businessidea import BusinessIdea
from foundation_tenant.models.tellusyourneed import TellUsYourNeed
from foundation_tenant.models.tag import Tag

from tenant_intake.decorators import tenant_intake_required


@login_required(login_url='/en/login')
@tenant_intake_required
def check_page(request):
    """Function will return either True or False depending if it meets decorator criteria."""
    from django.http import JsonResponse
    return JsonResponse({
        'access-granted':True
    })


@login_required(login_url='/en/login')
@group_required([constants.ENTREPRENEUR_GROUP_ID,])
def intake_entr_step_one_page(request):
    return render(request, 'tenant_intake/entrepreneur/1_view.html',{

    })
