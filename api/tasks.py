from celery import shared_task
from foundation_public.models.organization import PublicOrganization
from foundation_public.models.contactpoint import PublicContactPoint
from foundation_public.models.postaladdress import PublicPostalAddress
from foundation_public.models.organizationregistration import PublicOrganizationRegistration


# DEVELOPERS NOTE:
# (1) This file contains various asynchyonous processes that can be done by our system.


@shared_task
def begin_organization_creation_task(registered_id):
    """
    Asynchronously create our tenant schema. Email owner when process completes.
    """
    # Fetch our registered Organization.
    try:
        registered_org = PublicOrganizationRegistration.objects.get(id=int(registered_id))
    except PublicOrganization.DoesNotExist:
        return None

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
        name=registered_org.name
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

    return None
