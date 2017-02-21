from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.db.models import Q, Count
from foundation_tenant.utils import int_or_none
from foundation_tenant.models.base.calendarevent import CalendarEvent
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.tag import Tag
from smegurus import constants


@login_required(login_url='/en/login')
def reception_calendar_master_page(request):
    calendar_events = CalendarEvent.objects.filter(
        Q(pending__id=request.tenant_me.id) |
        Q(attendees__id=request.tenant_me.id) |
        Q(absentees__id=request.tenant_me.id)
    ).annotate(num_ids=Count('id')).order_by('-finish')  # Make unique and sort by latest.
    return render(request, 'tenant_reception/calendar/master/view.html',{
        'page': 'reception-calendar-master',
        'calendar_events': calendar_events
    })


@login_required(login_url='/en/login')
def reception_calendar_details_page(request, id):
    return render(request, 'tenant_reception/calendar/details/view.html',{
        'page': 'reception-calendar-details',
        'calendar_event': get_object_or_404(CalendarEvent, id=int(id)),
        'constants': constants,
    })
