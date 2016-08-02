from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from foundation_public.models.organization import PublicOrganization
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.message import Message


@login_required(login_url='/en/login')
@tenant_profile_required
def message_inbox_page(request):
    # print("TENANT", request.tenant.schema_name)
    # print("USER", request.user)
    return render(request, 'message/inbox_view.html',{
        'page': 'inbox',
        'organizations': PublicOrganization.objects.all(),
    })


@login_required(login_url='/en/login')
@tenant_profile_required
def message_compose_page(request):
    # print("TENANT", request.tenant.schema_name)
    # print("USER", request.user)
    return render(request, 'message/compose_view.html',{
        'page': 'composer',
        'organizations': PublicOrganization.objects.all(),
    })
