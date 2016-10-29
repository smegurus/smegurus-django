from django.utils import timezone
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
def inbox_page(request):
    # Fetch all the Messages and only get a single message per sender. Also ensure
    # that deleted messages are not returned.
    messages = Message.objects.filter(
        recipient=request.tenant_me,
        participants=request.tenant_me
    ).distinct('participants')
    return render(request, 'tenant_reception/message/master/view.html',{
        'page': 'inbox',
        'messages': messages,
    })


@login_required(login_url='/en/login')
def compose_page(request):
    admins = TenantMe.objects.filter(owner__groups__id=constants.ORGANIZATION_ADMIN_GROUP_ID)
    return render(request, 'tenant_reception/message/create/view.html',{
        'page': 'composer',
        'admins': admins,
        'recipient_id': 0,
    })


@login_required(login_url='/en/login')
def conversation_page(request, sender_id):
    messages = Message.objects.filter(
        Q(
            recipient=request.tenant_me,
            sender_id=int(sender_id),
            participants=request.tenant_me
        ) | Q(
            recipient_id=int(sender_id),
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

    return render(request, 'tenant_reception/message/detail/view.html',{
        'page': 'inbox',
        'messages': messages,
        'sender_id': sender_id,
    })
