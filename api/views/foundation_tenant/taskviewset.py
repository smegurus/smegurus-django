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
from api.serializers.foundation_tenant import TaskSerializer
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.task import Task
from foundation_tenant.models.orderedlogevent import OrderedLogEvent
from foundation_tenant.models.orderedcommentpost import OrderedCommentPost


class DateTimeSerializer(serializers.Serializer):
    date = serializers.DateTimeField(required=True,)
    is_start = serializers.BooleanField(required=True,)


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
        )

        # Update 'Task' model.
        task.participants.add(self.request.tenant_me)

        # Create "Ticket created" log event and attach it this Task.
        event = OrderedLogEvent.objects.create(
            me=self.request.tenant_me,
            text='Created Task #'+str(task.id),
            ip_address = self.request.META.get('REMOTE_ADDR')
        )
        task.log_events.add(event)

    def perform_update(self, serializer):
        """Update "TenantMe" model and its associated models."""
        # Update the 'Task' model.
        task = serializer.save()

        # Update associated models.
        if task.assignee:
            task.participants.add(task.assignee)

        # event = OrderedLogEvent.objects.create(
        #     me=self.request.tenant_me,
        #     text='Updated task #'+str(task.id)+' by '+task.assigned_by.name,
        #     ip_address = self.request.META.get('REMOTE_ADDR')
        # )
        # task.log_events.add(event)

    def perform_destroy(self, instance):
        """Override the deletion function to include deletion of associated models."""
        for log_event in instance.log_events.all():
            log_event.delete()
        instance.delete()  # Delete our model.

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def change_date(self, request, pk=None):
        try:
            serializer = DateTimeSerializer(data=request.data)
            if serializer.is_valid():
                task = self.get_object()
                text = ""
                is_start = serializer.data['is_start']
                if is_start:
                    text = "Change start date by " + str(request.tenant_me.name)
                    task.start = serializer.data['date']
                else:
                    text = "Change due date by " + str(request.tenant_me.name)
                    task.due = serializer.data['date']
                task.save()

                # Keep a log of change of date.
                event = OrderedLogEvent.objects.create(
                    me=self.request.tenant_me,
                    text=text,
                    ip_address = self.request.META.get('REMOTE_ADDR')
                )
                task.log_events.add(event)
        except Exception as e:
            print(e)



        return response.Response(
            data={'message': 'Task date has been changed.'},
            status=status.HTTP_200_OK
        )
