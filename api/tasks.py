from celery import shared_task
from django.core.management import call_command
from foundation_public.models.organizationregistration import PublicOrganizationRegistration


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

    # Send email to the owner of the Organization letting them know we've successfully
    # finished setting up their tenancy.
    call_command('send_organization_ready_email', str(registered_id))  # foundation_email/management/commands/send_organization_ready_email.py

    # Delete the registered organization.
    PublicOrganizationRegistration.objects.get(id=registered_id).delete()

    # Return nothing.
    return None


@shared_task
def begin_processing_document_task(doc_id, doc_type, schema_name, workspace_id):
    """
    Asynchronously process our document. Email owner when process completes.
    """
    # Run the sub-routine for taking the Document object and submitting it to
    # Bizmula "docxpresso" engine.

    if doc_type == 1:
        call_command('docxpresso_stage_01', schema_name, str(workspace_id))

    elif doc_type == 2:
        call_command('docxpresso_stage_02', schema_name, str(workspace_id))

    elif doc_type == 3:
        call_command('docxpresso_stage_03', schema_name, str(workspace_id))

    elif doc_type == 4:
        call_command('docxpresso_stage_04', schema_name, str(workspace_id))

    elif doc_type == 5:
        call_command('docxpresso_stage_05', schema_name, str(workspace_id))

    elif doc_type == 6:
        call_command('docxpresso_stage_06', schema_name, str(workspace_id))

    elif doc_type == 7:
        call_command('docxpresso_stage_07', schema_name, str(workspace_id))

    elif doc_type == 8:
        call_command('docxpresso_stage_08', schema_name, str(workspace_id))

    elif doc_type == 9:
        call_command('docxpresso_stage_09', schema_name, str(workspace_id))

    elif doc_type == 10:
        call_command('docxpresso_stage_10', schema_name, str(workspace_id))

    # Send email is ready email to the workspace owners.
    call_command('send_doc_ready_email', schema_name, str(doc_id))

    # Return nothing.
    return None


@shared_task
def begin_sending_pending_document_review_email_task(schema_name, doc_id):
    call_command('send_doc_pending_review_email', schema_name, str(doc_id))
    return None


@shared_task
def begin_send_accepted_document_review_notification_task(schema_name, doc_id):
    call_command('send_doc_acceptance_email', schema_name, str(doc_id))
    return None


@shared_task
def begin_send_rejection_document_review_notification_task(schema_name, doc_id):
    call_command('send_doc_rejection_email', schema_name, str(doc_id))
    return None
