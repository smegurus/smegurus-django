from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
from foundation_public.utils import latest_date_between
from foundation_tenant.models.communitypost import CommunityPost
from foundation_tenant.models.communityadvertisement import CommunityAdvertisement
from foundation_tenant.models.calendarevent import CalendarEvent
from foundation_tenant.models.message import Message
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.note import Note
from foundation_tenant.models.task_basic import TaskBasic


def my_last_modified_func(request):
    """
    Note: User my be authenticated.
    """
    # Get the last modified date for the User Profile.
    last_modified = request.tenant_me.last_modified

    # Compare with the Address.
    if request.tenant_me.address:
        last_modified = latest_date_between(last_modified, request.tenant_me.address.last_modified)

    # Compare with the ContactPoint.
    if request.tenant_me.contact_point:
        last_modified = latest_date_between(last_modified, request.tenant_me.contact_point.last_modified)
        last_modified = latest_date_between(last_modified, request.tenant_me.contact_point.last_modified)

    # Compare the last modified date per CalendarEvents.
    try:
        new_last_modified = CalendarEvent.objects.filter(
            owner=request.user,
        ).latest("last_modified").last_modified
        last_modified = latest_date_between(last_modified, new_last_modified)
    except CalendarEvent.DoesNotExist:
        pass

    # Compare the last modified date per CommunityPost.
    try:
        new_last_modified = CommunityPost.objects.filter(
            owner=request.user,
            me=request.tenant_me
        ).latest("last_modified").last_modified
        last_modified = latest_date_between(last_modified, new_last_modified)
    except CommunityPost.DoesNotExist:
        pass

    # Compare the last modified date per Message.
    try:
        new_last_modified = Message.objects.filter(
            participants__id=request.tenant_me.id
        ).latest("last_modified").last_modified
        last_modified = latest_date_between(last_modified, new_last_modified)
    except Message.DoesNotExist:
        pass

    # Compare the last modified date per Intake.
    try:
        new_last_modified = Intake.objects.latest("last_modified").last_modified
        last_modified = latest_date_between(last_modified, new_last_modified)
    except Intake.DoesNotExist:
        pass

    # Compare the last modified date per Intake.
    try:
        new_last_modified = Note.objects.latest("last_modified").last_modified
        last_modified = latest_date_between(last_modified, new_last_modified)
    except Note.DoesNotExist:
        pass

    # # Compare the last modified date per Task.
    # try:
    #     new_last_modified = Task.objects.filter(participants=request.tenant_me).latest("last_modified").last_modified
    #     last_modified = latest_date_between(last_modified, new_last_modified)
    # except Task.DoesNotExist:
    #     pass

    # Return the processed latest modified date
    return last_modified
