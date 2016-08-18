from datetime import datetime
from django.core.signing import Signer
from django.core.urlresolvers import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import condition
from foundation_tenant.models.me import TenantMe
from smegurus import constants


def user_last_login(request):
    return request.user.last_login


def get_activation_url(request):
    # Convert our User's ID into an encrypted value.
    # Note: https://docs.djangoproject.com/en/dev/topics/signing/
    signer = Signer()
    id_sting = str(request.user.id).encode()
    value = signer.sign(id_sting)

    # Generate our site's URL.
    url = 'https://' if request.is_secure() else 'http://'
    schema_name = request.tenant.schema_name
    if schema_name == 'public' or schema_name == 'test':
        url += "www."
    else:
        url += schema_name + "."
    url += get_current_site(request).domain
    url += reverse('foundation_auth_user_activation', args=[value,])
    url = url.replace("None","en")
    return url


@login_required(login_url='/en/login')
# @condition(last_modified_func=user_last_login)
def activate_page(request):
    template_url = 'foundation_auth/activate_org_admin.html'

    for my_group in request.user.groups.all():
        if constants.ENTREPRENEUR_GROUP_ID == my_group.id:
            template_url = 'foundation_auth/activate_entrepreneur.html'

    return render(request, template_url,{
        'user': request.user,
        'url': get_activation_url(request),
        'web_view_url': reverse('foundation_email_activate'),
    })
