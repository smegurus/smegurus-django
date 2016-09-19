from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import get_language
from django.contrib.auth.models import User


@login_required(login_url='/en/login')
def reception_dashboard_master_page(request):
    return render(request, 'tenant_reception/dashboard/master/view.html',{
        'page': 'reception-dashboard-master',
    })
