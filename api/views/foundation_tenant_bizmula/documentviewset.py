import django_filters
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.template.loader import render_to_string    # HTML to TXT
from django.core.mail import EmailMultiAlternatives    # EMAILER
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import detail_route
from api.pagination import LargeResultsSetPagination
from api.permissions import EmployeePermission
from api.serializers.foundation_tenant_bizmula import DocumentSerializer
from api.serializers.misc import JudgementSerializer
from foundation_public.utils import resolve_full_url_with_subdmain
from foundation_tenant.models.bizmula.document import Document
from smegurus.settings import env_var
from smegurus import constants


class SendEmailViewMixin(object):
    def send_rejected_document_review_notification(self, document):
        """
        Function will send a "Pending Document Review" email to the Documents
        assigned Advisor.
        """
        # Iterate through all owners of this document and generate the contact
        # list for all the Entrepreneurs.
        contact_list = []
        for me in document.workspace.mes.all():
            contact_list.append(me.owner.email)

        # Generate the data.
        url =  resolve_full_url_with_subdmain(
            self.request.tenant.schema_name,
            'foundation_auth_user_login',
            []
        )
        web_view_extra_url = resolve_full_url_with_subdmain(
            self.request.tenant.schema_name,
            'foundation_email_rejected_document',
            [document.id,]
        )
        subject = "Rejected Document"
        param = {
            'user': self.request.user,
            'document': document,
            'url': url,
            'web_view_url': web_view_extra_url,
        }

        # Plug-in the data into our templates and render the data.
        text_content = render_to_string('tenant_review/rejected_doc_review.txt', param)
        html_content = render_to_string('tenant_review/rejected_doc_review.html', param)

        # Generate our address.
        from_email = env_var('DEFAULT_FROM_EMAIL')
        to = contact_list

        # Send the email.
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class DocumentFilter(django_filters.FilterSet):
    class Meta:
        model = Document
        fields = ['workspace', 'document_type', 'status']


class DocumentViewSet(SendEmailViewMixin, viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = DocumentFilter

    # def perform_create(self, serializer):
    #     """Add owner to the object when being created for the first time"""
    #     # Include the owner attribute directly, rather than from request data.
    #     workspace = serializer.save()
    #     workspace.owners.add(self.request.user)
    #     workspace.save()

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def run_docgen(self, request, pk=None):
        """Function will generate the document in DocGen."""
        try:
            document = self.get_object()

            #TODO: IMPLEMENT.

            return response.Response(status=status.HTTP_200_OK)  # Return the success indicator.
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated, EmployeePermission,])
    def judge(self, request, pk=None):
        """
        Grant employee the ability to set the status of this document.
        """
        try:
            serializer = JudgementSerializer(data=request.data)
            if serializer.is_valid():
                # Update the document.
                document = self.get_object()
                document.status = serializer.data['status']
                document.description = serializer.data['comment']
                document.save()

                # Send acceptance notification.
                if document.status == constants.DOCUMENT_READY_STATUS:
                    # self.send_document_reviewed_notification(document)  #TODO: IMPLEMENT NOTIFICATION

                    # If the document is a master document for this Module then
                    # send a notification email to the assigned Advisor.
                    if document.document_type.is_master:
                        document.workspace.stage_num += 1
                        document.workspace.save()
                        for me in document.workspace.mes.all():
                            me.stage_num += 1
                            me.save()

                # Send rejection notification.
                if document.status == constants.DOCUMENT_CREATED_STATUS:
                    self.send_rejected_document_review_notification(document)

                # Send success response.
                return response.Response(status=status.HTTP_200_OK)
            else:
                raise Exception('Inputted data is not valid.')
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
