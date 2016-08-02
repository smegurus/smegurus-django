from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from foundation_public.models.organization import PublicOrganization
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.message import Message
from foundation_tenant.models.me import TenantMe
from foundation_public import constants
from django.db.models import Max
from django.db.models import Count
@login_required(login_url='/en/login')
@tenant_profile_required
def message_inbox_page(request):
    # Fetch all the Messages and only get a single message per sender. Also ensure
    # that deleted messages are not returned.
    messages = Message.objects.filter(recipient=request.tenant_me, is_archived=False).distinct('sender')
    return render(request, 'tenant_message/inbox/view.html',{
        'page': 'inbox',
        'messages': messages,
    })


@login_required(login_url='/en/login')
@tenant_profile_required
def message_compose_page(request):
    entrepreneurs = TenantMe.objects.filter(owner__groups__id=constants.ENTREPRENEUR_GROUP_ID)
    mentors = TenantMe.objects.filter(owner__groups__id=constants.MENTOR_GROUP_ID)
    advisors = TenantMe.objects.filter(owner__groups__id=constants.ADVISOR_GROUP_ID)
    managers = TenantMe.objects.filter(owner__groups__id=constants.ORGANIZATION_MANAGER_GROUP_ID)
    admins = TenantMe.objects.filter(owner__groups__id=constants.ORGANIZATION_ADMIN_GROUP_ID)
    return render(request, 'tenant_message/composer/view.html',{
        'page': 'composer',
        'entrepreneurs': entrepreneurs,
        'mentors': mentors,
        'advisors': advisors,
        'managers': managers,
        'admins': admins,
    })
from django.db.models import Q

@login_required(login_url='/en/login')
@tenant_profile_required
def conversation_page(request, sender_id):
    messages = Message.objects.filter(
        Q(
            recipient=request.tenant_me,
            is_archived=False,
            sender_id=int(sender_id),
        ) | Q(
            recipient=int(sender_id),
            is_archived=False,
            sender_id=request.tenant_me,
        ),
    )
    return render(request, 'tenant_message/conversation/view.html',{
        'page': 'inbox',
        'messages': messages,
        'sender_id': sender_id,
    })
