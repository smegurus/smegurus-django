from django.shortcuts import render
from foundation_public.models.organization import PublicOrganization
# from foundation.decorators import tenant_required


def land_page(request):
    print("TENANT", request.tenant.schema_name)
    print("USER", request.user)
    return render(request, 'landpage/landpage.html',{
        'organizations': PublicOrganization.objects.all(),
    })


def term_page(request):
    print("TENANT", request.tenant.schema_name)
    print("USER", request.user)
    return render(request, 'landpage/landpage.html',{
        'organizations': PublicOrganization.objects.all(),
    })
