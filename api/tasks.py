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

    # Send email to the owner of the Organization letting them know we've successfully
    # finished setting up their tenancy.
    call_command('send_organization_ready_email', str(registered_id))  # foundation_email/management/commands/send_organization_ready_email.py

    # Return nothing.
    return None


@shared_task
def begin_processing_document_task(doc_id, doc_type, schema_name):
    """
    Asynchronously process our document. Email owner when process completes.
    """
    # print("DOC_ID", doc_id)
    # print("DOC_TYPE", doc_type)
    # print("TENANT", schema_name)

    # Run the sub-routine for taking the Document object and submitting it to
    # Bizmula "docxpresso" engine.

    # 1. Entrepreneur Self Assessment
    if doc_type == 1:
        print("TODO: Entrepreneur Self Assessment")

    # 2. Market Research Summary
    if doc_type == 2:
        call_command('docxpresso_doc_type_02', schema_name, str(doc_id))

    # 3. Market Research Plan
    if doc_type == 3:
        print("TODO: Market Research Plan")

    # 4. Concept Validation
    if doc_type == 4:
        print("TODO: Concept Validation")

    # 5. Marketing
    if doc_type == 5:
        print("TODO: Marketing")

    # 6. Sales
    if doc_type == 6:
        print("TODO: Sales")

    # 7. Operations
    if doc_type == 7:
        print("TODO: Operations")

    # Send email is ready email to the workspace owners.
    call_command('send_doc_ready_email', schema_name, str(doc_id))

    # Return nothing.
    return None


@shared_task
def begin_setting_pending_document_for_review_task(schema_name, doc_id):
    """
    Asynchronously process our document. Email owner when process completes.
    """
    call_command('pending_doc_review', schema_name, str(doc_id))
    return None
