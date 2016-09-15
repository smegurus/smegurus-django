from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from foundation_public.models.organization import PublicOrganization
# from foundation.decorators import tenant_required


@staff_member_required
def organization_menu_page(request):
    # print("TENANT", request.tenant.schema_name)
    # print("USER", request.user)
    return render(request, 'public_admin/organization/menu_view.html',{
        'organizations': PublicOrganization.objects.all(),
    })


@staff_member_required
def organization_create_page(request):
    return render(request, 'public_admin/organization/create/view.html',{
        'organizations': PublicOrganization.objects.all(),
    })


@staff_member_required
def organization_master_page(request):
    return render(request, 'public_admin/organization/master/view.html',{
        'organizations': PublicOrganization.objects.all(),
    })
