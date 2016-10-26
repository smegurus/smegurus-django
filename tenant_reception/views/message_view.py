from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.translation import get_language
from django.contrib.auth.models import User, Group
from foundation_tenant.utils import int_or_none
from foundation_tenant.models.message import Message
from foundation_tenant.models.me import TenantMe
from smegurus import constants


@login_required(login_url='/en/login')
def message_master_page(request):
    admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
    admin = TenantMe.objects.get(owner__groups=admin_group)
    messages = Message.objects.filter(
        Q(
            recipient=request.tenant_me,
            sender_id=int(admin.id),
            participants=request.tenant_me
        ) | Q(
            recipient_id=int(admin.id),
            sender_id=request.tenant_me,
            participants=request.tenant_me
        )
    ).order_by("created")

    # Recipients have the ability to update the 'date_read'.
    for message in messages.all():
        if message.recipient == request.tenant_me:
            # Give the message the read-time.
            message.date_read = timezone.now()
            message.save()

    return render(request, 'tenant_reception/message/master/view.html',{
        'page': 'inbox',
        'messages': messages,
        'sender_id': admin.id,
    })
