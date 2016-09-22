from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.views.decorators.http import condition
from django.db.models import Q
from rest_framework.authtoken.models import Token
from foundation_tenant.utils import my_last_modified_func
from tenant_configuration.decorators import tenant_configuration_required
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from foundation_tenant.utils import int_or_none
from foundation_tenant.models.calendarevent import CalendarEvent
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.tag import Tag
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def calendar_master_page(request):
    events = CalendarEvent.objects.filter(
        Q(owner=request.user) | Q(attendees__id=request.tenant_me.id) | Q(pending__id=request.tenant_me.id)
    )
    return render(request, 'tenant_calendar/master/view.html',{
        'page': 'calendar',
        'events': events,
        'my_events': CalendarEvent.objects.filter(owner=request.user),
        'pending_events': CalendarEvent.objects.filter(pending__id=request.tenant_me.id),
        'attending_events': CalendarEvent.objects.filter(attendees__id=request.tenant_me.id),
        'absentee_events': CalendarEvent.objects.filter(absentees__id=request.tenant_me.id),
        'constants': constants,
    })


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def calendar_create_page(request):
    return render(request, 'tenant_calendar/create/view.html',{
        'page': 'calendar',
        'all_profiles': TenantMe.objects.all(),
        'tags': Tag.objects.filter(is_program=True),
        'type_of': int_or_none(request.GET.get('type_of')),
        'constants': constants
    })


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def calendar_edit_details_page(request, id):
    return render(request, 'tenant_calendar/details/edit/view.html',{
        'page': 'calendar',
        'calendar_items': CalendarEvent.objects.filter(owner=request.user),
        'calendar_event': get_object_or_404(CalendarEvent, id=int(id)),
        'all_profiles': TenantMe.objects.all(),
        'constants': constants,
    })


@login_required(login_url='/en/login')
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=my_last_modified_func)
def calendar_info_details_page(request, id):
    return render(request, 'tenant_calendar/details/info/view.html',{
        'page': 'calendar',
        'calendar_items': CalendarEvent.objects.filter(owner=request.user),
        'calendar_event': get_object_or_404(CalendarEvent, id=int(id)),
        'all_profiles': TenantMe.objects.all(),
        'constants': constants,
    })
