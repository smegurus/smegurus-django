import random
import base64
import hashlib
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
from smegurus.settings import env_var
from smegurus import constants


def get_unique_username_from_email(email):
    """
    Uniquely generate our 'username' by taking the email and create a hash.
    Source: https://github.com/dabapps/django-email-as-username/blob/master/emailusernames/utils.py
    """
    email = email.lower()  # Emails should be case-insensitive unique
    converted = email.encode('utf8', 'ignore')  # Deal with internationalized email addresses
    return base64.urlsafe_b64encode(hashlib.sha256(converted).digest())[:30]


def get_pretty_formatted_date(created):
    if created == None:
        return "-"

    today = timezone.now()
    dt = (today - created).days
    if dt == 0:
        return _("Today")
    elif dt < 60 and dt > 0:
        return _("%(dt)s days ago") % { 'dt' : dt }
    else:
        return str(created)


def latest_date_between(date_1, date_2):
    """Utility function to compare the dates and return latest date."""
    if date_1 > date_2:
        return date_1
    else:
        return date_2


def latest_date_in(array):
    latest = array[0]
    for date in array:
        latest = latest_date_between(latest, date)
    return latest


def random_text(size):
    """Randomly generate text"""
    alphabet_and_numbers = 'abcdefghijklmnopqrstuvwqyz1234567890'
    return(''.join(random.choice(alphabet_and_numbers) for _ in range(size)))


def resolve_full_url_with_subdmain(schema_name, reverse_url_id, resolve_url_args): #TODO: Write Unit Tests for this.
    """
    Enhanced "reverse" function which will include the HTTP PROTOCAL and HTTP
    DOMAIN for the reversed link with subdomain
    """
    url = env_var('SMEGURUS_APP_HTTP_PROTOCOL')
    url += schema_name + "."
    url += env_var('SMEGURUS_APP_HTTP_DOMAIN')
    url += reverse(reverse_url_id, args=resolve_url_args)
    url = url.replace("None","en")
    return url
