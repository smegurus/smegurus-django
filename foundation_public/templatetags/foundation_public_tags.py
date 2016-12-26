# -*- coding: utf-8 -*-
from django import template
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import resolve, reverse # Reverse
from django.contrib.sites.models import Site
from foundation_public.utils import get_pretty_formatted_date
from smegurus.settings import env_var


register = template.Library()


@register.simple_tag
def tenant_url(schema_name, view_name):
    http_protocol = 'https://' if env_var("SECURE_SSL_REDIRECT") else 'http://'
    if schema_name:
        return http_protocol + schema_name + '.%s' % Site.objects.get_current().domain + reverse(view_name)
    else:
        return http_protocol + '%s' % Site.objects.get_current().domain + reverse(view_name)


@register.filter
def pretty_formatted_date(date):
    return get_pretty_formatted_date(date)


@register.simple_tag
def get_app_public_domain():
    """
    Returns the full URL to the domain. The output from this function gets
    generally appended with a path string.
    """
    http_protocol = 'http://'
    return http_protocol + '%s' % Site.objects.get_current().domain



@register.simple_tag
def get_app_tenant_domain(organization):
    """
    Reverse the URL of the request + view name for this Organization.
    """
    from django.contrib.sites.shortcuts import get_current_site # Reverse
    from django.core.urlresolvers import resolve, reverse # Reverse
    from django.contrib.sites.models import Site
    from smegurus.settings import env_var

    http_protocol = 'https://' if env_var("SECURE_SSL_REDIRECT") else 'http://'
    if organization.schema_name:
        return http_protocol + organization.schema_name + '.%s' % Site.objects.get_current().domain
    else:
        return http_protocol + '%s' % Site.objects.get_current().domain
