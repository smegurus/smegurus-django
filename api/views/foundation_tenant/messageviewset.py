import django_filters
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import filters
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import detail_route
from api.permissions import IsMessageObjectPermission
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant import MessageSerializer
from foundation_tenant.models.message import Message


class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = ['created', 'last_modified', 'owner', 'name', 'alternate_name',
                  'description', 'url', 'sender', 'recipient',
                  'is_archived_by_sender', 'is_archived_by_recipient',]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.filter()
    serializer_class = MessageSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsMessageObjectPermission)
    filter_class = MessageFilter

    def perform_create(self, serializer):
        """Add owner to this model when being created for the first time"""
        # Include the owner attribute directly, rather than from request data.
        instance = serializer.save(
            owner=self.request.user,
            sender=self.request.tenant_me,
        )

    def perform_destroy(self, instance):
        """Override the deletion function to archive the message instead of deleting it."""
        if self.request.user.is_authenticated():
            if self.request.tenant_me == instance.sender:
                instance.is_archived_by_sender = True
            if self.request.tenant_me == instance.recipient:
                instance.is_archived_by_recipient = True
            instance.save()
