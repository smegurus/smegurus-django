from django.http import HttpResponseForbidden
from foundation_public.models.banned import BannedIP
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint


class TenantMeMiddleware(object):
    def process_request(self, request):
        """
            The purpose of this middleware is to lookup the 'Me' object for
            the authenticated user and attach it to the request. If the user
            is authenticated and does not have a 'Me' object then it will be
            created in this middleware.
        """
        if not request.tenant.schema_name in ['public', 'test']:
            if request.user.is_authenticated():
                tenant_me, created = TenantMe.objects.get_or_create(owner=request.user)
                request.tenant_me = tenant_me

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
                    tenant_me.save()

        return None  # Finish our middleware handler.
