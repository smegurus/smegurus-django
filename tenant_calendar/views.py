from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from foundation_config.decorators import foundation_config_required
from foundation_tenant.models.calendarevent import CalendarEvent


@foundation_config_required
@login_required(login_url='/en/login')
def calendar_page(request):
    return render(request, 'tenant_calendar/view.html',{
        'page': 'calendar',
        'calendar_items': CalendarEvent.objects.filter(owner=request.user)
    })
