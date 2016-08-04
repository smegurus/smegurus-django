from django.utils import timezone
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from foundation_public.models.organization import PublicOrganization
from tenant_profile.decorators import tenant_profile_required
from foundation_tenant.models.message import Message
from foundation_tenant.models.me import TenantMe
from foundation_public import constants


@login_required(login_url='/en/login')
@tenant_profile_required
def inbox_page(request):
    # Fetch all the Messages and only get a single message per sender. Also ensure
    # that deleted messages are not returned.
    messages = Message.objects.filter(
        recipient=request.tenant_me,
        participants=request.tenant_me
    ).distinct('participants')
    return render(request, 'tenant_message/message/master_view.html',{
        'page': 'inbox',
        'messages': messages,
    })


@login_required(login_url='/en/login')
@tenant_profile_required
def compose_page(request):
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


@login_required(login_url='/en/login')
@tenant_profile_required
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

            # Decrement the new message counter to indicate User has read the
            # message.
            if message.recipient.unread_messages_count > 0:
                message.recipient.unread_messages_count = message.recipient.unread_messages_count - 1
                message.recipient.save()

    return render(request, 'tenant_message/message/details_view.html',{
        'page': 'inbox',
        'messages': messages,
        'sender_id': sender_id,
    })


@login_required(login_url='/en/login')
@tenant_profile_required
def archive_conversation_page(request, sender_id):
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

    # Iterate through all the messages and removes the person from the conversation. (A.k.a.: archived)
    for message in messages.all():
        message.participants.remove(request.tenant_me)
        message.save()

    # Redirect his page.
    return HttpResponseRedirect(reverse('tenant_message_inbox'))


@login_required(login_url='/en/login')
@tenant_profile_required
def archive_list_page(request):
    # Fetch all the Messages and only get a single message per sender. Also ensure
    # that deleted messages are not returned.
    messages = Message.objects.filter(
        Q(
            recipient=request.tenant_me
        ) &~  # and not
        Q(
            participants=request.tenant_me
        )
    ).distinct('participants')
    return render(request, 'tenant_message/archive/master_view.html',{
        'page': 'archive',
        'messages': messages,
    })


@login_required(login_url='/en/login')
@tenant_profile_required
def archive_details_page(request, sender_id):
    messages = Message.objects.filter(
        Q(
            Q(
                recipient=request.tenant_me,
                sender_id=int(sender_id),
            ) &~  # and not
            Q(
                participants=request.tenant_me
            )
        ) |
        Q(
            Q(
                recipient_id=int(sender_id),
                sender_id=request.tenant_me,
            ) &~  # and not
            Q(
                participants=request.tenant_me
            )
        )
    ).order_by("created")
    return render(request, 'tenant_message/archive/details_view.html',{
        'page': 'archive',
        'messages': messages,
        'sender_id': sender_id,
    })
