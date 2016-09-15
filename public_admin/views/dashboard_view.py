from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def dashboard_master_page(request):
    return render(request, 'public_admin/dashboard/master/view.html',{})
