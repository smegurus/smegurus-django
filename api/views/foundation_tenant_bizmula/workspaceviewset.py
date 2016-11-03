import django_filters
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant_bizmula import WorkspaceSerializer
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.documenttype import DocumentType


class WorkspaceFilter(django_filters.FilterSet):
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'owners',]


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
        workspace.owners.add(self.request.user)
        workspace.save()

        # Create the documents for our system.
        document_types = DocumentType.objects.all()
        for document_type in document_types.all():
            Document.objects.create(
                workspace=workspace,
                document_type=document_type,
                name=str(document_type),
                is_ready=False
            )
