import django_filters
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant_bizmula import DocumentSerializer
from foundation_tenant.models.bizmula.document import Document


class DocumentFilter(django_filters.FilterSet):
    class Meta:
        model = Document
        fields = ['workspace', 'document_type', 'is_ready']


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
