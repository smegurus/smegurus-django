from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
from foundation_public.utils import latest_date_between
from foundation_tenant.models.base.communitypost import CommunityPost
from foundation_tenant.models.base.communityadvertisement import CommunityAdvertisement
from foundation_tenant.models.base.calendarevent import CalendarEvent
from foundation_tenant.models.base.message import Message
from foundation_tenant.models.base.me import TenantMe
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.note import Note
from foundation_tenant.models.base.task import Task


def get_pretty_formatted_date(created):
    today = timezone.now()
    dt = (today - created).days
    if dt == 0:
        return _("Today")
    elif dt < 60 and dt > 0:
        return _("%(dt)s days ago") % { 'dt' : dt }
    else:
        return str(created)


def int_or_none(value):
    try:
        return int(value)
    except Exception as e:
        return None
