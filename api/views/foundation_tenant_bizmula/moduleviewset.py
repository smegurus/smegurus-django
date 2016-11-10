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
from api.permissions import ManagementOrAuthenticatedReadOnlyPermission
from api.serializers.foundation_tenant_bizmula import ModuleSerializer
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from smegurus import constants


class ModuleFilter(django_filters.FilterSet):
    class Meta:
        model = Module
        fields = ['stage_num', 'title', 'description', 'icon', 'colour']


class ModuleViewSet(viewsets.ModelViewSet):
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
    def finish(self, request, pk=None):
        """
        Function will iterate through all the Documents for this Module.
        """
        try:
            # Get our Module object.
            module = self.get_object()

            # Fetch all the Documents for this Module belonging to the
            # currently authenticated User.
            documents = Document.objects.filter(
                workspace__stage_num=module.stage_num,
                workspace__owners__id=request.user.id
            )

            # Iterate through all the documents inside this Module belonging
            # to the authenticated User and process the Document.
            for document in documents.all():
                document.status = constants.DOCUMENT_PENDING_REVIEW_STATUS
                document.save()

                # If the document is a master document for this Module then
                # send a notification email to the assigned Advisor.
                if document.document_type.is_master:
                    pass  #TODO: Implement. notification for Advisors.

            return response.Response(status=status.HTTP_200_OK)  # Return the success indicator.
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
