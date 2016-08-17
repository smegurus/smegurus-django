import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import detail_route
from rest_framework import exceptions, serializers
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrIsAnEmployee
from api.serializers.foundation_tenant import TaskSerializer, OrderedLogEventSerializer, OrderedCommentPostSerializer
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.task import Task
from foundation_tenant.models.orderedlogevent import OrderedLogEvent
from foundation_tenant.models.orderedcommentpost import OrderedCommentPost


# class DateTimeSerializer(serializers.Serializer):
#     date = serializers.IntegerField(required=True,)
#     comment = serializers.CharField(max_length=2055, required=False,)
#     is_employee_created = serializers.BooleanField(default=False, required=False,)



class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['created', 'last_modified', 'owner', 'name',
                  'description', 'image', 'assigned_by',
                  'assignee', 'status', 'participants', 'tags',
                  'start', 'due', 'comment_posts',]


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
        task = serializer.save(
            owner=self.request.user,
            assigned_by=self.request.tenant_me,
            assignee=self.request.tenant_me,
            status=constants.ASSIGNED_TASK_STATUS,
        )

        # Update 'Task' model.
        task.participants.add(self.request.tenant_me)

        # Create "Ticket created" log event and attach it this Task.
        event = OrderedLogEvent.objects.create(
            me=self.request.tenant_me,
            text='Created Task #'+str(task.id)
        )
        task.log_events.add(event)

    def perform_update(self, serializer):
        """Update "TenantMe" model and its associated models."""
        # Update the 'Task' model.
        task = serializer.save()

        # Update associated models.
        if task.assignee:
            task.participants.add(task.assignee)

    def perform_destroy(self, instance):
        """Override the deletion function to include deletion of associated models."""
        for log_event in instance.log_events.all():  # Delete associated models.
            log_event.delete()
        for post in instance.comment_posts.all():
            post.delete()
        instance.delete()  # Delete our model.

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def log_event(self, request, pk=None):
        try:
            serializer = OrderedLogEventSerializer(data=request.data)
            if serializer.is_valid():
                log_event = serializer.save(me=self.request.tenant_me)
                task = self.get_object()
                task.log_events.add(log_event)
                return response.Response(status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(
                data={'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    # @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    # def post_comment(self, request, pk=None):
    #     pass #TODO: IMplement.
