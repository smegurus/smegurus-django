import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrIsAnEmployee
from api.serializers.foundation_tenant import TaskSerializer
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.task import Task
from foundation_tenant.models.note import Note
from foundation_tenant.models.calendarevent import CalendarEvent


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['created', 'last_modified', 'owner', 'name',
                  'description', 'image', 'note', 'event',
                  'assigned_by', 'assignee', 'status',]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrIsAnEmployee, )
    filter_class = TaskFilter

    def perform_create(self, serializer):
        """Override the creation function to include creation of associated models."""
        # Create 'Task' models.
        instance = serializer.save(
            owner=self.request.user,
            assigned_by=self.request.tenant_me,
        )

        # Create associated models.
        if not instance.note:
            instance.note = Note.objects.create(
                owner=self.request.user,
                me=self.request.tenant_me,
            )
        if not instance.event:
            instance.event = CalendarEvent.objects.create(
                owner=self.request.user,
            )

        # Update 'Task' model.
        instance.participants.add(self.request.tenant_me)
        instance.save()

    def perform_destroy(self, instance):
        """Override the deletion function to include deletion of associated models."""
        # Delete associated models.
        if instance.note:
            instance.note.delete()

        if instance.event:
            instance.event.delete()

        instance.delete()  # Delete our model.
