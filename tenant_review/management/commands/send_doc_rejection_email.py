import json
import urllib3  # Third Party Library
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.bizmula.documenttype import DocumentType
from foundation_tenant.models.bizmula.question import Question
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.slide import Slide
from foundation_tenant.models.bizmula.questionanswer import QuestionAnswer
from foundation_tenant.models.base.me import TenantMe
from foundation_public.utils import resolve_full_url_with_subdmain
from foundation_tenant.utils import int_or_none
from smegurus import constants


from django.template.loader import render_to_string    # HTML to TXT
from django.core.mail import EmailMultiAlternatives    # EMAILER


class Command(BaseCommand):
    help = _('Perform a verdict on a document.')

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+')

    def handle(self, *args, **options):
        """
        Function will get the inputted tenant name and doc_id and
        set the database to the tenant schema and begin processing
        for the particular document.
        """
        schema_name = options['id'][0]
        doc_id = int_or_none(options['id'][1])

        # the tenant metadata is stored.
        from django.db import connection

        # Connection will set it back to our tenant.
        connection.set_schema(schema_name, True) # Switch to Tenant.

        try:
            with transaction.atomic():
                # Fetch our document.
                doc = Document.objects.get(id=doc_id)

                # Take our document and submit the answers to Docxpresso.
                self.begin_processing(schema_name, doc)
        except Document.DoesNotExist:
            raise CommandError(_('Cannot find document #%s.' % doc_id))
        except Exception as e:
            raise CommandError(_('Unknown error occured.'))

    def begin_processing(self, schema_name, document):
        """
        Function will send a "Rejected Document Review" email to the Documents
        assigned Advisor.
        """
        # Iterate through all owners of this document and generate the contact
        # list for all the Entrepreneurs.
        contact_list = []
        for me in document.workspace.mes.all():
            contact_list.append(me.owner.email)

        # Generate the data.
        url =  resolve_full_url_with_subdmain(
            schema_name,
            'foundation_auth_user_login',
            []
        )
        web_view_extra_url = resolve_full_url_with_subdmain(
            schema_name,
            'foundation_email_rejected_document',
            [document.id,]
        )
        subject = "Rejected Document"
        param = {
            'document': document,
            'url': url,
            'web_view_url': web_view_extra_url,
        }

        # Plug-in the data into our templates and render the data.
        text_content = render_to_string('tenant_review/rejected_doc_review.txt', param)
        html_content = render_to_string('tenant_review/rejected_doc_review.html', param)

        # Generate our address.
        from_email = settings.DEFAULT_FROM_EMAIL
        to = contact_list

        # Send the email.
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # Return a success message to the console.
        self.stdout.write(
            self.style.SUCCESS(_('Sent Document #%s judgement email.') % str(document.id))
        )
