import pytz
from django.utils import timezone
from django.http import HttpResponseForbidden
from foundation_public.models.banned import BannedIP
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.imageupload import TenantImageUpload
from foundation_tenant.models.visitor import TenantVisitor


def me(request):
    """
    The purpose of this context processor is to lookup the 'Me' object for
    the authenticated user and attach it to the request. If the user
    is authenticated and does not have a 'Me' object then it will be
    created in this middleware.
    """
    tenant_me = None
    if not request.tenant.schema_name in ['public', 'test']:
        if request.user.is_authenticated():
            # STEP 1: Get or create a TenantMe.
            tenant_me, created = TenantMe.objects.get_or_create(owner=request.user)

            # STEP 2: Populate the TenantMe object.
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
                tenant_me.image = TenantImageUpload.objects.create(
                    owner=request.user,
                )
                tenant_me.save()

    return {
        'tenant_me': tenant_me,
    }


def timezone(request):
    """
    The purpose of this context processor is to set the timezone of this
    Organization's timezone to be the timezone of the User's session.
    """
    if not request.tenant.schema_name in ['public', 'test']:
        # Source:
        # https://docs.djangoproject.com/en/dev/topics/i18n/timezones/#selecting-the-current-time-zone
        tzname = request.tenant.time_zone
        timezone.activate(pytz.timezone(tzname))
    return {}
