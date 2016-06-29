from django.shortcuts import render
from foundation.decorators import tenant_required


def land_page(request):
    print("TENANT", request.tenant.schema_name)
    print("USER", request.user)
    return render(request, 'landpage/landpage.html',{

    })
