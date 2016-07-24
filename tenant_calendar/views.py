from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from foundation_config.decorators import foundation_config_required
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.calendarevent import CalendarEvent


@login_required(login_url='/en/login')
@foundation_config_required
@tenant_profile_required
def calendar_page(request):
    return render(request, 'tenant_calendar/view.html',{
        'page': 'calendar',
        'calendar_items': CalendarEvent.objects.filter(owner=request.user)
    })
