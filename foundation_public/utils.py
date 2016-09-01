import base64
import hashlib
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta


def get_unique_username_from_email(email):
    """
    Uniquely generate our 'username' by taking the email and create a hash.
    Source: https://github.com/dabapps/django-email-as-username/blob/master/emailusernames/utils.py
    """
    email = email.lower()  # Emails should be case-insensitive unique
    converted = email.encode('utf8', 'ignore')  # Deal with internationalized email addresses
    return base64.urlsafe_b64encode(hashlib.sha256(converted).digest())[:30]


def get_pretty_formatted_date(created):
    today = timezone.now()
    dt = (today - created).days
    if dt == 0:
        return _("Today")
    elif dt < 60 and dt > 0:
        return _("%(dt)s days ago") % { 'dt' : dt }
    else:
        return str(created)


def latest_between_dates(date_1, date_2):
    """Utility function to compare the dates and return latest date."""
    if date_1 > date_2:
        return date_1
    else:
        return date_2
