import django_filters
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
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
    def task_url(self, schema_name, task):
        """Function will return the URL to the task page through the sub-domain of the organization."""
        url = 'https://' if self.request.is_secure() else 'http://'
        url += schema_name + "."
        url += get_current_site(self.request).domain
        url += task.get_absolute_url()
        url = url.replace("None","en")
        return url

    def send_notification(self, schema_name, task, log_event):
        # Iterate through all the participants in the Task and get their
        # email only if they request email notification for taks.
        contact_list = []
        for me in task.participants.all():
            if me.notify_when_task_had_an_interaction:
                contact_list.append(me.owner.email)

        # Generate our email body text.
        subject = 'Task #'+str(task.id)
        url = self.task_url(schema_name, task)
        html_text = _('%(log_text)s.\n\n To see the Task, click here: %(url)s') % {'log_text':str(log_event.text), 'url': str(url)}

        # Send the email.
        send_mail(
            subject,
            html_text,
            env_var('DEFAULT_FROM_EMAIL'),
            contact_list,
            fail_silently=False
        )


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
        self.send_notification(self.request.tenant.schema_name, task, log_event)

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
                # Create the 'OrderedLogEvent' model and save it.
                log_event = serializer.save(me=request.tenant_me)
                task = self.get_object()
                task.log_events.add(log_event)

                # Send email notification for event.
                self.send_notification(request.tenant.schema_name, task, log_event)

                # Send success response.
                return response.Response(status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(
                data={'message': str(e)},
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
                self.send_notification(request.tenant.schema_name, task, log_event)

                # Return the success indicator.
                return response.Response(status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(
                data={'message': str(e)},
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
            self.send_notification(request.tenant.schema_name, task, log_event)

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
            self.send_notification(request.tenant.schema_name, task, log_event)

            # Return the success indicator.
            return response.Response(status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
