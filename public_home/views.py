from django.shortcuts import render
from foundation_public.models.organization import PublicOrganization
# from foundation.decorators import tenant_required


def index_page(request):
    # print("TENANT", request.tenant.schema_name)
    # print("USER", request.user)
    return render(request, 'public_home/index_view.html',{
        'organizations': PublicOrganization.objects.all(),
    })


def start_page(request):
    return render(request, 'public_home/start_view.html',{
        'organizations': PublicOrganization.objects.all(),
    })


def term_page(request):
    # print("TENANT", request.tenant.schema_name)
    # print("USER", request.user)
    return render(request, 'public_home/terms_view.html',{})


def http_403_page(request):
    return render(request, 'public_home/403_view.html',{})


def http_404_page(request):
    return render(request, 'public_home/404_view.html',{})


def http_500_page(request):
    return render(request, 'public_home/500_view.html',{})
