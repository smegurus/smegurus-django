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
from api.permissions import IsOwnerOrIsAnEmployee, EmployeePermission
from api.serializers.foundation_tenant import TaskSerializer, SortedLogEventByCreatedSerializer, SortedCommentPostByCreatedSerializer
from api.serializers.misc import DateTimeSerializer, IntegerSerializer
from foundation_tenant.models.fileupload import TenantFileUpload
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.task import Task
from foundation_tenant.models.logevent import SortedLogEventByCreated
from foundation_tenant.models.commentpost import SortedCommentPostByCreated
from foundation_tenant.models.calendarevent import CalendarEvent
from smegurus.settings import env_var
from smegurus import constants


class SendEmailViewMixin(object):
    def get_web_view(self, task, log_event):
        url = 'https://' if self.request.is_secure() else 'http://'
        url += self.request.tenant.schema_name + "."
        url += get_current_site(self.request).domain
        url += reverse('foundation_email_task', args=[task.id, log_event.id,])
        return url

    def get_task_url(self, task):
        """Function will return the URL to the task page through the sub-domain of the organization."""
        url = 'https://' if self.request.is_secure() else 'http://'
        url += self.request.tenant.schema_name + "."
        url += get_current_site(self.request).domain
        url += reverse('tenant_task_details_info', args=[task.id,])
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
            'web_view_url': self.get_web_view(task, log_event),
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
                  'description', 'image', 'status', 'type_of', 'participants',
                  'start', 'is_due', 'due', 'tags', 'assigned_by', 'opening',
                  'closures', 'comment_posts', 'log_events', 'uploads', 'resources',]


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
        )

        # Add myself to the participants.
        task.participants.add(self.request.tenant_me)

        # If this task is by group invite, then take the groups and
        # assign the Users from each group into this event.
        if task.type_of == constants.TASK_BY_TAG_TYPE:
            for tag in task.tags.all():
                try:
                    me = TenantMe.objects.get(tags__id=tag.id)
                    task.opening.add(me)
                except Exception as e:
                    pass

        # All assigned Users are added to the participants list.
        for me in task.opening.all():
            task.participants.add(me)

        # Create "Ticket created" log event and attach it this Task.
        log_event = SortedLogEventByCreated.objects.create(
            me=self.request.tenant_me,
            text='Created \"'+str(task.name)+"\" task."
        )
        task.log_events.add(log_event)

    def perform_update(self, serializer):
        """Update "TenantMe" model and its associated models."""
        task = serializer.save()  # Update the 'Task' model.

        # Add myself to the participants.
        task.participants.add(self.request.tenant_me)

        # All assigned Users are added to the participants list.
        for me in task.opening.all():
            task.participants.add(me)
        for me in task.closures.all():
            task.participants.add(me)

    def perform_destroy(self, instance):
        """Override the deletion function to include deletion of associated models."""
        for log_event in instance.log_events.all():  # Delete associated models.
            log_event.delete()
        for post in instance.comment_posts.all():
            post.delete()
        for file_upload in instance.uploads.all():
            file_upload.delete()
        instance.delete()  # Delete our model.

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def log_event(self, request, pk=None):
        try:
            serializer = SortedLogEventByCreatedSerializer(data=request.data)
            if serializer.is_valid():
                # Create the 'SortedLogEventByCreated' model and save it.
                log_event = serializer.save(me=request.tenant_me)
                task = self.get_object()
                task.log_events.add(log_event)

                # Send email notification for specific events.
                if 'Created' in log_event.text:
                    self.send_notification(task, log_event)

                # Send success response.
                return response.Response(status=status.HTTP_200_OK)
            else:
                raise Exception('Inputted data is not valid.')
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def post_comment(self, request, pk=None):
        try:
            serializer = SortedCommentPostByCreatedSerializer(data=request.data)
            if serializer.is_valid():
                # Save the comment.
                comment_post = serializer.save(me=request.tenant_me)
                task = self.get_object()
                task.comment_posts.add(comment_post)

                # Save an log event.
                text = request.tenant_me.name + " has made a comment."
                log_event = SortedLogEventByCreated.objects.create(
                    me=request.tenant_me,
                    text=text,
                )
                task.log_events.add(log_event)

                # Add myself to the participants.
                task.participants.add(request.tenant_me)

                # Send email notification for log event.
                self.send_notification(task, log_event)

                # Return the success indicator.
                return response.Response(status=status.HTTP_200_OK)
            else:
                raise Exception('Inputted data is not valid.')
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def close(self, request, pk=None):
        """Function will place the User into the closure list from the opening list."""
        try:
            task = self.get_object()  # Get Task and update it's status.
            task.opening.remove(request.tenant_me)
            task.closures.add(request.tenant_me)
            return response.Response(status=status.HTTP_200_OK)  # Return the success indicator.
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def open(self, request, pk=None):
        """Function will place the User into the opening list from the closure list."""
        try:
            task = self.get_object()  # Get Task and update it's status.
            task.opening.add(request.tenant_me)
            task.closures.remove(request.tenant_me)
            return response.Response(status=status.HTTP_200_OK)  # Return the success indicator.
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['put'], permission_classes=[EmployeePermission])
    def complete(self, request, pk=None):
        """Function will mark this Task as 'CLOSED_TASK_STATUS'."""
        try:
            task = self.get_object()  # Get Task and update it's status.
            task.status = constants.CLOSED_TASK_STATUS
            task.save()

            # Save an log event.
            text = request.tenant_me.name + " has changed the status to be completed."
            log_event = SortedLogEventByCreated.objects.create(
                me=request.tenant_me,
                text=text,
            )
            task.log_events.add(log_event)

            self.send_notification(task, log_event)  # Send email notification for log event.
            return response.Response(status=status.HTTP_200_OK)  # Return the success indicator.
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['put'], permission_classes=[EmployeePermission])
    def incomplete(self, request, pk=None):
        """Function will mark this Task as 'INCOMPLETE_TASK_STATUS'."""
        try:
            # Get Task and update it's status.
            task = self.get_object()
            task.status = constants.OPEN_TASK_STATUS
            task.save()

            # Save an log event.
            text = request.tenant_me.name + " has changed the status to be incompleted."
            log_event = SortedLogEventByCreated.objects.create(
                me=request.tenant_me,
                text=text,
            )
            task.log_events.add(log_event)
            self.send_notification(task, log_event)  # Send email notification for log event.
            return response.Response(status=status.HTTP_200_OK)  # Return the success indicator.
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def attach_file(self, request, pk=None):
        """Function will place the User into the opening list from the closure list."""
        try:
            serializer = IntegerSerializer(data=request.data)
            if serializer.is_valid():
                # Lookup file.
                upload_id = serializer.data['value']
                file_upload = TenantFileUpload.objects.get(id=upload_id)

                # Attach file.
                task = self.get_object()
                task.uploads.add(file_upload)
                task.save()

                # Return the success indicator.
                return response.Response(status=status.HTTP_200_OK)
            else:
                raise Exception('Inputted data is not valid.')
        except Exception as e:
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
