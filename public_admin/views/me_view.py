from django.shortcuts import render
from foundation_public.models.organization import PublicOrganization
# from foundation.decorators import tenant_required

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard_master_page(request):
    # print("TENANT", request.tenant.schema_name)
    # print("USER", request.user)
    return render(request, 'public_admin/dashboard/master/view.html',{
        'organizations': PublicOrganization.objects.all(),
    })
