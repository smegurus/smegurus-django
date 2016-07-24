from django.shortcuts import render
from foundation_public.models.organization import PublicOrganization
# from foundation.decorators import tenant_required
from tenant_profile.decorators import tenant_profile_required


@tenant_profile_required
def message_inbox_page(request):
    # print("TENANT", request.tenant.schema_name)
    # print("USER", request.user)
    return render(request, 'message/inbox_view.html',{
        'page': 'inbox',
        'organizations': PublicOrganization.objects.all(),
    })


@tenant_profile_required
def message_compose_page(request):
    # print("TENANT", request.tenant.schema_name)
    # print("USER", request.user)
    return render(request, 'message/compose_view.html',{
        'page': 'composer',
        'organizations': PublicOrganization.objects.all(),
    })
