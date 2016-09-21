from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.views.decorators.http import condition
from rest_framework.authtoken.models import Token
from foundation_tenant.utils import my_last_modified_func
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from foundation_tenant.models.calendarevent import CalendarEvent
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def calendar_master_page(request):
    return render(request, 'tenant_calendar/master/view.html',{
        'page': 'calendar',
        'calendar_items': CalendarEvent.objects.filter(owner=request.user, status__gte=constants.APPROVED_STATUS)
    })


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def calendar_details_page(request, id):
    return render(request, 'tenant_calendar/details/view.html',{
        'page': 'calendar',
        'calendar_items': CalendarEvent.objects.filter(owner=request.user),
        'calendar_event': get_object_or_404(CalendarEvent, id=int(id)),
    })
