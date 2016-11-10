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
from api.serializers.foundation_tenant_bizmula import WorkspaceSerializer
from api.serializers.misc import IntegerSerializer
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.documenttype import DocumentType


class WorkspaceFilter(django_filters.FilterSet):
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'mes', 'stage_num']


class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    filter_class = WorkspaceFilter

    def perform_create(self, serializer):
        """Add owner to the object when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        workspace = serializer.save()
        workspace.mes.add(self.request.tenant_me)
        workspace.save()

        # Create the documents for our system.
        document_types = DocumentType.objects.all()
        for document_type in document_types.all():
            Document.objects.create(
                workspace=workspace,
                document_type=document_type,
                name=str(document_type)
            )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated, EmployeePermission])
    def set_stage_num(self, request, pk=None):
        """Function will set the 'stage_num' for this workspace."""
        try:
            serializer = IntegerSerializer(data=request.data)
            if serializer.is_valid():
                # Update the document.
                workspace = self.get_object()
                workspace.stage_num = int(serializer.data['value'])
                workspace.save()

                # Send success response.
                return response.Response(status=status.HTTP_200_OK)
            else:
                raise Exception('Inputted data is not valid.')
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
