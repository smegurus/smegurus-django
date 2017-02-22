import os
import sys
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection # Used for django tenants.
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.organization import PublicOrganization
from foundation_public.models.contactpoint import PublicContactPoint
from foundation_public.models.postaladdress import PublicPostalAddress
from foundation_public.models.organizationregistration import PublicOrganizationRegistration


class Command(BaseCommand):
    help = _('Creates a tenant for the inputted organization registration id.')

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+')

    def handle(self, *args, **options):
        # Connection needs first to be at the public schema, as this is where
        # the database needs to be set before creating a new tenant. If this is
        # not done then django-tenants will raise a "Can't create tenant outside
        # the public schema." error.
        connection.set_schema_to_public() # Switch to Public.

        # Fetch our registered Organization.
        for registered_id in options['id']:
            try:
                registered_org = PublicOrganizationRegistration.objects.get(id=int(registered_id))
                self.begin_processing(registered_org)
            except PublicOrganizationRegistration.DoesNotExist:
                raise CommandError(_('Organization registration doest not exist at specificed ID'))

    def begin_processing(self, registered_org):
        owner = registered_org.owner

        # Create our associated models.
        contact_point, created = PublicContactPoint.objects.get_or_create(owner=owner)
        address, created = PublicPostalAddress.objects.get_or_create(owner=owner)


        # Create our Tenant and have Django-Tenants create the schema for this
        # Organization in our database.
        org = PublicOrganization.objects.create(
            owner=owner,
            contact_point=contact_point,
            address=address,
            schema_name=registered_org.schema_name,
            legal_name=registered_org.name
        )

        # Perform a custom post-save action.
        # Our tenant requires a domain so create it here.
        from django.contrib.sites.models import Site
        from foundation_public.models.organization import PublicDomain
        domain = PublicDomain()
        domain.domain = org.schema_name + '.' + Site.objects.get_current().domain
        domain.tenant = org
        domain.is_primary = False
        domain.save()

        # Override custom default values.
        org.has_mentors = True
        org.has_perks = True
        org.is_setup = False

        # Attach our current logged in User for our Organization.
        org.users.add(owner)
        org.save()

        self.stdout.write(
            self.style.SUCCESS(_('Successfully created organization tenant.'))
        )
