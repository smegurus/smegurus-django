import django_filters
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string    # HTML to TXT
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives    # Emailer
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
from smegurus.settings import env_var
from smegurus import constants


class SendEmailViewMixin(object):
    def get_task_url(self, task):
        """Function will return the URL to the task page through the sub-domain of the organization."""
        url = 'https://' if self.request.is_secure() else 'http://'
        url += self.request.tenant.schema_name + "."
        url += get_current_site(self.request).domain
        url += reverse('tenant_task_details', args=[task.id,])
        url = url.replace("None","en")
        return url

    def send_notification(self, task, log_event):
        # Iterate through all the participants in the Task and get their
        # email only if they request email notification for taks.
        contact_list = []
        for me in task.participants.all():
            if me.notify_when_task_had_an_interaction:
                contact_list.append(me.owner.email)

        # Generate the data.
        subject = "Task #" + str(task.id)
        param = {
            'user': self.request.user,
            'task': task,
            'log_event': log_event,
            'url': self.get_task_url(task),
            'web_view_url': reverse('foundation_email_task', args=[task.id, log_event.id,]),
        }

        # Plug-in the data into our templates and render the data.
        text_content = render_to_string('tenant_task/task.html', param)
        html_content = render_to_string('tenant_task/task.html', param)

        # Generate our address.
        from_email = env_var('DEFAULT_FROM_EMAIL')
        to = contact_list

        # Send the email.
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['created', 'last_modified', 'owner', 'name',
                  'description', 'image', 'assigned_by',
                  'assignee', 'status', 'participants', 'tags',
                  'start', 'due', 'comment_posts',]


class TaskViewSet(SendEmailViewMixin, viewsets.ModelViewSet):
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
        log_event = OrderedLogEvent.objects.create(
            me=self.request.tenant_me,
            text='Created Task #'+str(task.id)
        )
        task.log_events.add(log_event)

        # Send email notification for 'OrderedLogEvent' model.
        self.send_notification(task, log_event)

    def perform_update(self, serializer):
        """Update "TenantMe" model and its associated models."""
        task = serializer.save()  # Update the 'Task' model.
        if task.assignee:
            task.participants.add(task.assignee)  # Update associated models.

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
                # Create the 'OrderedLogEvent' model and save it.
                log_event = serializer.save(me=request.tenant_me)
                task = self.get_object()
                task.log_events.add(log_event)

                # Send email notification for event.
                self.send_notification(task, log_event)

                # Send success response.
                return response.Response(status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def post_comment(self, request, pk=None):
        try:
            serializer = OrderedCommentPostSerializer(data=request.data)
            if serializer.is_valid():
                # Save the comment.
                comment_post = serializer.save(me=request.tenant_me)
                task = self.get_object()
                task.comment_posts.add(comment_post)

                # Save an log event.
                text = request.tenant_me.name + " has made a comment."
                log_event = OrderedLogEvent.objects.create(
                    me=request.tenant_me,
                    text=text,
                )
                task.log_events.add(log_event)

                # Add the user to the participants.
                task.participants.add(request.tenant_me)

                # Send email notification for log event.
                self.send_notification(task, log_event)

                # Return the success indicator.
                return response.Response(status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def complete_task(self, request, pk=None):
        """Function will mark this Task as 'COMPLETED_TASK_STATUS'."""
        try:
            # Get Task and update it's status.
            task = self.get_object()
            task.status = constants.COMPLETED_TASK_STATUS
            task.save()

            # Save an log event.
            text = request.tenant_me.name + " has changed the status to be completed."
            log_event = OrderedLogEvent.objects.create(
                me=request.tenant_me,
                text=text,
            )
            task.log_events.add(log_event)

            # Send email notification for log event.
            self.send_notification(task, log_event)

            # Return the success indicator.
            return response.Response(status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def incomplete_task(self, request, pk=None):
        """Function will mark this Task as 'INCOMPLETE_TASK_STATUS'."""
        try:
            # Get Task and update it's status.
            task = self.get_object()
            task.status = constants.INCOMPLETE_TASK_STATUS
            task.save()

            # Save an log event.
            text = request.tenant_me.name + " has changed the status to be incompleted."
            log_event = OrderedLogEvent.objects.create(
                me=request.tenant_me,
                text=text,
            )
            task.log_events.add(log_event)

            # Send email notification for log event.
            self.send_notification(task, log_event)

            # Return the success indicator.
            return response.Response(status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
