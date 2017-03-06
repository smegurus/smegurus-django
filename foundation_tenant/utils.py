import time
import base64
import hashlib
from django.conf import settings
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.signing import Signer
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import crypto
from django.utils import timezone
from django.utils.translation import to_locale, get_language
from django.utils.translation import ugettext_lazy as _
from babel.numbers import format_number
from foundation_public.utils import latest_date_between


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


def float_or_none(value):
    try:
        return float(value)
    except Exception as e:
        return None


def get_random_string(length=31,
                    allowed_chars='abcdefghijkmnpqrstuvwxyz'
                                       'ABCDEFGHIJKLMNPQRSTUVWXYZ'
                                       '23456789'):
    """
    Random string generator simplified from Django.
    """
    return crypto.get_random_string(length, allowed_chars)


def django_sign(plaintext_value):
    """
    Function will take the plaintext value and sign with the django SECRET_KEY.
    """
    # Convert our User's ID into an encrypted value.
    # Note: https://docs.djangoproject.com/en/dev/topics/signing/
    signer = Signer()
    id_sting = str(plaintext_value).encode()
    return signer.sign(id_sting)


def django_unsign(signed_value):
    """
    Function will take the signed value and get the plaintext value by cheching
    this django SECRET_KEY.
    """
    try:
        # Convert our signed value into a text.
        signer = Signer()
        return signer.unsign(signed_value)
    except Exception as e:
        return 0


def is_email_unique(email):
    """
    Utility function checks to see if parameter email is unique or not.
    """
    return not User.objects.filter(email=email).exists()


def generate_hash():
    """
    Utility function generate will generate a hash on a timestamp.
    """
    hash = hashlib.sha1()
    time_str = str(time.time())
    utf8_time_str = time_str.encode('utf-8')
    hash.update(utf8_time_str)
    return  hash.hexdigest()


from django.contrib.humanize.templatetags.humanize import intcomma


def currency(dollars):
    """
    http://stackoverflow.com/a/2180209
    """
    dollars = round(float(dollars), 2)
    return "$%s%s" % (intcomma(int(dollars)), ("%0.2f" % dollars)[-3:])


def humanize_number(number, locale = None):
    """
    Utility function which will take a integer/float value and convert it
    into a humanized format.
    """
    if locale is None:
        lang = get_language()
        if lang is None:
            lang = "en"
        locale = to_locale(lang)
    return format_number(number, locale = locale)
