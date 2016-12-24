from celery import shared_task
from django.core.management import call_command


# DEVELOPERS NOTE:
# (1) This file contains various asynchyonous processes that can be done by our system.


@shared_task
def begin_organization_creation_task(registered_id):
    """
    Asynchronously create our tenant schema. Email owner when process completes.
    """
    # Run the sub-routine for taking the OrganizationRegistration object
    # creating our Tenant from it.
    call_command('populate_organization', str(registered_id))  # foundation_public/management/commands/populate_organization.py

    # Return nothing.
    return None
