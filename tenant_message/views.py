from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.http import condition
from foundation_public.models.organization import PublicOrganization
from tenant_profile.decorators import tenant_profile_required
from tenant_intake.decorators import tenant_intake_required
from tenant_reception.decorators import tenant_reception_required
from tenant_configuration.decorators import tenant_configuration_required
from foundation_tenant.decorators import tenant_required
from foundation_tenant.models.base.message import Message
from foundation_tenant.models.base.me import Me
from smegurus import constants


@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
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
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def compose_page(request):
    entrepreneurs = Me.objects.filter(owner__groups__id=constants.ENTREPRENEUR_GROUP_ID)
    mentors = Me.objects.filter(owner__groups__id=constants.MENTOR_GROUP_ID)
    advisors = Me.objects.filter(owner__groups__id=constants.ADVISOR_GROUP_ID)
    managers = Me.objects.filter(owner__groups__id=constants.ORGANIZATION_MANAGER_GROUP_ID)
    admins = Me.objects.filter(owner__groups__id=constants.ORGANIZATION_ADMIN_GROUP_ID)
    return render(request, 'tenant_message/composer/generic_view.html',{
        'page': 'composer',
        'entrepreneurs': entrepreneurs,
        'mentors': mentors,
        'advisors': advisors,
        'managers': managers,
        'admins': admins,
        'recipient_id': 0,
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
def specific_compose_page(request, id):
    entrepreneurs = Me.objects.filter(owner__groups__id=constants.ENTREPRENEUR_GROUP_ID)
    mentors = Me.objects.filter(owner__groups__id=constants.MENTOR_GROUP_ID)
    advisors = Me.objects.filter(owner__groups__id=constants.ADVISOR_GROUP_ID)
    managers = Me.objects.filter(owner__groups__id=constants.ORGANIZATION_MANAGER_GROUP_ID)
    admins = Me.objects.filter(owner__groups__id=constants.ORGANIZATION_ADMIN_GROUP_ID)
    recipient = get_object_or_404(Me,pk=id)
    return render(request, 'tenant_message/composer/specific_view.html',{
        'page': 'composer',
        'entrepreneurs': entrepreneurs,
        'mentors': mentors,
        'advisors': advisors,
        'managers': managers,
        'admins': admins,
        'recipient': recipient,
    })


@login_required()
@tenant_required
def latest_conversation_details(request, sender_id):
    return Message.objects.filter(
        Q(
            recipient=request.tenant_me,
            sender_id=int(sender_id),
            participants=request.tenant_me
        ) | Q(
            recipient_id=int(sender_id),
            sender_id=request.tenant_me,
            participants=request.tenant_me
        )
    ).latest("last_modified").last_modified


@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
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

    return render(request, 'tenant_message/message/details_view.html',{
        'page': 'inbox',
        'messages': messages,
        'sender_id': sender_id,
    })


@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
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


@login_required()
@tenant_required
def latest_archived_message_master(request):
    try:
        return Message.objects.filter(
            Q(
                recipient=request.tenant_me
            ) &~  # and not
            Q(
                participants=request.tenant_me
            )
        ).latest("last_modified").last_modified
    except Message.DoesNotExist:
        return datetime.now()


@login_required(login_url='/en/login')
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
# @condition(last_modified_func=latest_archived_message_master)
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
@tenant_required
@tenant_intake_required
@tenant_reception_required
@tenant_profile_required
@tenant_configuration_required
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
