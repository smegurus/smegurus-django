from celery import shared_task
from foundation_public.models.organization import PublicOrganization
from foundation_public.models.contactpoint import PublicContactPoint
from foundation_public.models.postaladdress import PublicPostalAddress

# DEVELOPERS NOTE:
# (1) This file contains various asynchyonous processes that can be done by our system.

@shared_task
def begin_organization_creation_task(dict):
    """
    Asynchronously create our tenant schema. Email owner when process completes.
    """
    pass
    # Create our Tenant and have Django-Tenants create the schema for this
    # Organization in our database.
    # org = serializer.save(
    #     owner=owner,
    #     contact_point=contact_point,
    #     address=address,
    # )
    #
    # # Perform a custom post-save action.
    # if org:
    #     # Our tenant requires a domain so create it here.
    #     from django.contrib.sites.models import Site
    #     from foundation_public.models.organization import PublicDomain
    #     domain = PublicDomain()
    #     domain.domain = org.schema_name + '.' + Site.objects.get_current().domain
    #     domain.tenant = org
    #     domain.is_primary = False
    #     domain.save()
    #
    #     # Override custom default values.
    #     org.has_mentors = True
    #     org.has_perks = True
    #     org.is_setup = False
    #
    #     # Attach our current logged in User for our Organization.
    #     org.users.add(owner)
    #     org.save()
    #
    return None
