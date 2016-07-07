# -*- coding: utf-8 -*-
from django import template
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import resolve, reverse # Reverse
from django.contrib.sites.models import Site
from smegurus.settings import env_var


register = template.Library()


@register.simple_tag
def tenant_url(schema_name, view_name):
    http_protocol = 'https://' if env_var("SECURE_SSL_REDIRECT") else 'http://'
    if schema_name:
        return http_protocol + schema_name + '.%s' % Site.objects.get_current().domain + reverse(view_name)
    else:
        return http_protocol + '%s' % Site.objects.get_current().domain + reverse(view_name)
