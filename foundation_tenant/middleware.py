import pytz
from django.utils import timezone
from foundation_tenant.models.base.me import TenantMe
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


class TenantMeMiddleware(object):
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
                # STEP 1: Get or create a TenantMe.
                tenant_me, created = TenantMe.objects.get_or_create(owner=request.user)
                request.tenant_me = tenant_me

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
                    tenant_me.image = ImageUpload.objects.create(
                        owner=request.user,
                    )

                    # STEP 3: Update profile that staff users are managed by themselves.
                    if tenant_me.is_employee():
                        tenant_me.managed_by = tenant_me

                    # STEP 4: SAVE
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
