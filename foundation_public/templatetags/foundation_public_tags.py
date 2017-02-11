# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import resolve, reverse
from django.contrib.sites.models import Site
from foundation_public.utils import get_pretty_formatted_date
from smegurus.settings import env_var


register = template.Library()


@register.simple_tag
def tenant_url(schema_name, view_name):
    if schema_name:
        return settings.SMEGURUS_APP_HTTP_PROTOCOL + schema_name + '.%s' % settings.SMEGURUS_APP_HTTP_DOMAIN + reverse(view_name)
    else:
        return settings.SMEGURUS_APP_HTTP_PROTOCOL + '%s' % settings.SMEGURUS_APP_HTTP_DOMAIN + reverse(view_name)


@register.filter
def pretty_formatted_date(date):
    return get_pretty_formatted_date(date)


@register.simple_tag
def get_app_public_domain():
    """
    Returns the full URL to the domain. The output from this function gets
    generally appended with a path string.
    """
    return settings.SMEGURUS_APP_HTTP_PROTOCOL + '%s' % settings.SMEGURUS_APP_HTTP_DOMAIN



@register.simple_tag
def get_app_tenant_domain(organization):
    """
    Reverse the URL of the request + view name for this Organization.
    """
    if organization.schema_name:
        return settings.SMEGURUS_APP_HTTP_PROTOCOL + organization.schema_name + '.%s' % settings.SMEGURUS_APP_HTTP_DOMAIN
    else:
        return settings.SMEGURUS_APP_HTTP_PROTOCOL + '%s' % settings.SMEGURUS_APP_HTTP_DOMAIN
