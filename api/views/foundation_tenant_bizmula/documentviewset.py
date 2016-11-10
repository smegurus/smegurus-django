import django_filters
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
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
from foundation_tenant.models.bizmula.document import Document
from smegurus import constants


class DocumentFilter(django_filters.FilterSet):
    class Meta:
        model = Document
        fields = ['workspace', 'document_type', 'status']


class DocumentViewSet(viewsets.ModelViewSet):
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

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def has_pending_review(self, request, pk=None):
        try:
            document = self.get_object()
            document.status = constants.DOCUMENT_PENDING_REVIEW_STATUS
            document.save()
            return response.Response(status=status.HTTP_200_OK)  # Return the success indicator.
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated, EmployeePermission,])
    def judge(self, request, pk=None):
        """Grant employee the ability to set the status of this document."""
        try:
            serializer = JudgementSerializer(data=request.data)
            if serializer.is_valid():
                # Update the document.
                document = self.get_object()
                document.status = serializer.data['status']
                document.description = serializer.data['comment']
                document.save()

                # Send success response.
                return response.Response(status=status.HTTP_200_OK)
            else:
                raise Exception('Inputted data is not valid.')
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )