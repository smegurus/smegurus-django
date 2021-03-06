# -*- coding: utf-8 -*-
import pytz
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.contactpoint import ContactPoint
from foundation_tenant.models.base.imageupload import ImageUpload
from foundation_tenant.models.base.visitor import Visitor


class TenantTimezoneMiddleware(object):
    """Sets the timezone per Organization."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.tenant.schema_name in ['public', 'test']:
            # Source:
            # https://docs.djangoproject.com/en/dev/topics/i18n/timezones/#selecting-the-current-time-zone
            tzname = request.tenant.time_zone
            timezone.activate(pytz.timezone(tzname))
        return self.get_response(request)


class MeMiddleware(object):
    """
        The purpose of this middleware is to lookup the 'Me' object for
        the authenticated user and attach it to the request. If the user
        is authenticated and does not have a 'Me' object then it will be
        created in this middleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.tenant.schema_name in ['public', 'test']:
            if request.user.is_authenticated():
                # STEP 1: Security, ensure the authenticated user belongs to this org.
                if request.user not in request.tenant.users.all():
                    # Step I: Load depedency
                    from django.http import HttpResponseForbidden
                    from django.contrib.auth import logout

                    # Step II: Close the Django session.
                    logout(request)

                    # Step III:
                    return HttpResponseForbidden(_('You do not belong to this organizaiton.'))

                # STEP 2: Get or create a Me.
                tenant_me, created = Me.objects.get_or_create(owner=request.user)
                request.tenant_me = tenant_me

                # STEP 3: Populate the Me object.
                if created:
                    tenant_me.name = request.user.first_name+' '+request.user.last_name
                    tenant_me.given_name = request.user.first_name
                    tenant_me.family_name = request.user.last_name
                    tenant_me.email = request.user.email
                    tenant_me.address = PostalAddress.objects.create(
                        owner=request.user,
                        name='User #' + str(request.user.id) + ' Address',
                    )
                    tenant_me.contact_point = ContactPoint.objects.create(
                        owner=request.user,
                        name='User #' + str(request.user.id) + ' Contact Point',
                    )
                    tenant_me.image = ImageUpload.objects.create(
                        owner=request.user,
                    )

                    # STEP 4: Update profile that staff users are managed by themselves.
                    if tenant_me.is_employee():
                        tenant_me.managed_by = tenant_me

                    # STEP 5: SAVE
                    tenant_me.save()
        return self.get_response(request)


class VisitorMiddleware(object):
    """The purpose of this middleware is to save what the User sees."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.tenant.schema_name in ['public', 'test']:
            if request.user.is_authenticated():
                Visitor.objects.create(
                    me=request.tenant_me,
                    path=request.path,
                    ip_address=request.ip_address
                )
        return self.get_response(request)
