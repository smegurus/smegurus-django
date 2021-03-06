import django_filters
import django_rq
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.template.loader import render_to_string    # HTML to TXT
from django.core.mail import EmailMultiAlternatives    # EMAILER
from django.core.management import call_command
from django.db import transaction
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import detail_route
from api.pagination import LargeResultsSetPagination
from api.permissions import ManagementOrAuthenticatedReadOnlyPermission
from api.serializers.foundation_tenant_bizmula import ModuleSerializer
from api.tasks import begin_processing_document_task
from foundation_public.utils import resolve_full_url_with_subdmain
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.base.me import Me
from smegurus.settings import env_var
from smegurus import constants


class SendEmailViewMixin(object):
    def send_pending_document_review_notification(self, document):
        """
        Function will send a "Pending Document Review" email to the Documents
        assigned Advisor.
        """
        # Fetch the original administrator for this Organization.
        org_admin_user = User.objects.filter(groups__id=constants.ORGANIZATION_ADMIN_GROUP_ID).earliest('date_joined')

        # Iterate through all owners of this document and generate the contact
        # list for all the Advisors for each Entrepreneur.
        contact_list = []
        for me in document.workspace.mes.all():
            # If this User profile has an assigned manager then add this person
            # to the email else just email the administrator.
            if me.managed_by:
                contact_list.append(me.managed_by.owner.email)
            else:
                contact_list.append(org_admin_user.email)

                # Assign the original admininistrator User to this unmanaged user.
                me.managed_by = Me.objects.get(owner=org_admin_user)
                me.save()

        # Generate the data.
        url =  resolve_full_url_with_subdmain(
            self.request.tenant.schema_name,
            'tenant_review_detail',
            [document.id,]
        )
        web_view_extra_url = resolve_full_url_with_subdmain(
            self.request.tenant.schema_name,
            'foundation_email_pending_document',
            [document.id,]
        )
        subject = "Pending Document Review"
        param = {
            'user': self.request.user,
            'document': document,
            'url': url,
            'web_view_url': web_view_extra_url,
        }

        # Plug-in the data into our templates and render the data.
        text_content = render_to_string('tenant_review/pending_doc_review.txt', param)
        html_content = render_to_string('tenant_review/pending_doc_review.html', param)

        # Generate our address.
        from_email = env_var('DEFAULT_FROM_EMAIL')
        to = contact_list

        # Send the email.
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class ModuleFilter(django_filters.FilterSet):
    class Meta:
        model = Module
        fields = ['stage_num', 'title', 'description', 'icon', 'colour']


class ModuleViewSet(SendEmailViewMixin, viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, ManagementOrAuthenticatedReadOnlyPermission)
    filter_class = ModuleFilter

    # def perform_create(self, serializer):
    #     """Add owner to the object when being created for the first time"""
    #     # Include the owner attribute directly, rather than from request data.
    #     workspace = serializer.save()
    #     workspace.owners.add(self.request.user)
    #     workspace.save()

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def generate_docxpresso_doc(self, request, pk=None):
        """
        Function will iterate through all the submitted Documents for this
        Module and set them to be reviewed by the advisor. Note: Advisor will
        only get a notification when a master document is detected.
        """
        try:
            # Get our Module object.
            module = self.get_object()

            # Fetch all the Documents for this Module belonging to the
            # currently authenticated User.
            documents = Document.objects.filter(
                document_type__stage_num=module.stage_num,
                workspace__mes=request.tenant_me
            )

            # Iterate through all the documents inside this Module belonging
            # to the authenticated User and process the Document.
            for document in documents.all():
                django_rq.enqueue(
                    begin_processing_document_task,
                    document.id,
                    document.document_type.id,
                    request.tenant.schema_name,
                    document.workspace.id
                )

            return response.Response(status=status.HTTP_200_OK)  # Return the success indicator.
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def finish(self, request, pk=None):
        try:
            with transaction.atomic():
                # Get our Module object.
                module = self.get_object()

                # Fetch all the Documents for this Module belonging to the
                # currently authenticated User.
                documents = Document.objects.filter(
                    document_type__stage_num=module.stage_num,
                    workspace__mes=request.tenant_me
                )

                # Process asynchyonously.
                from api.tasks import begin_sending_pending_document_review_email_task
                from api.tasks import begin_send_accepted_document_review_notification_task

                # Iterate through all the documents inside this Module belonging
                # to the authenticated User and process the Document.
                for document in documents.all():

                    # DEVELOPERS NOTE:
                    # - If the administrator wants automatic approval of document
                    #   reviews and no longer have advisors review the document then
                    #   the following code will be run.
                    # - Else document needs to be approved by the advisor.
                    if request.tenant.has_staff_checkin_required:

                        document.status = constants.DOCUMENT_PENDING_REVIEW_STATUS
                        document.save()
                        django_rq.enqueue(begin_sending_pending_document_review_email_task,
                            request.tenant.schema_name,
                            document.id
                        )

                    else:

                        # Change document type.
                        document.status = constants.DOCUMENT_READY_STATUS

                        # Add simple comment.
                        document.doc = "Automatically approved."

                        # Save the document.
                        document.save()

                        # Send acceptance email.
                        django_rq.enqueue(begin_send_accepted_document_review_notification_task,
                            request.tenant.schema_name,
                            document.pk
                        )

                        # Update all the workspaces.
                        max_stage_num = module.stage_num + 1  # Set to the next stage level.
                        document.workspace.stage_num = max_stage_num
                        document.workspace.save()
                        for me in document.workspace.mes.all():
                            if me.stage_num < max_stage_num:
                                me.stage_num = max_stage_num
                                me.save()


            return response.Response(status=status.HTTP_200_OK)  # Return the success indicator.
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
