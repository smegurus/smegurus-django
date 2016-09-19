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
from api.serializers.foundation_tenant import LearningTaskSerializer
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.learningtask import LearningTask
from smegurus.settings import env_var
from smegurus import constants


class SendEmailViewMixin(object):
    def get_web_view(self, task, log_event):
        url = 'https://' if self.request.is_secure() else 'http://'
        url += self.request.tenant.schema_name + "."
        url += get_current_site(self.request).domain
        url += reverse('foundation_email_task', args=[task.id, log_event.id,])
        return url
#
#     def get_task_url(self, task):
#         """Function will return the URL to the task page through the sub-domain of the organization."""
#         url = 'https://' if self.request.is_secure() else 'http://'
#         url += self.request.tenant.schema_name + "."
#         url += get_current_site(self.request).domain
#         url += reverse('tenant_task_details', args=[task.id,])
#         url = url.replace("None","en")
#         return url
#
#     def send_notification(self, task, log_event):
#         # Iterate through all the participants in the Task and get their
#         # email only if they request email notification for taks.
#         contact_list = []
#         for me in task.participants.all():
#             if me.notify_when_task_had_an_interaction:
#                 contact_list.append(me.owner.email)
#
#         # Generate the data.
#         subject = "Task #" + str(task.id)
#         param = {
#             'user': self.request.user,
#             'task': task,
#             'log_event': log_event,
#             'url': self.get_task_url(task),
#             'web_view_url': self.get_web_view(task, log_event),
#         }
#
#         # Plug-in the data into our templates and render the data.
#         text_content = render_to_string('tenant_task/task.html', param)
#         html_content = render_to_string('tenant_task/task.html', param)
#
#         # Generate our address.
#         from_email = env_var('DEFAULT_FROM_EMAIL')
#         to = contact_list
#
#         # Send the email.
#         msg = EmailMultiAlternatives(subject, text_content, from_email, to)
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()


class LearningTaskFilter(django_filters.FilterSet):
    class Meta:
        model = LearningTask
        fields = ['id', 'created', 'last_modified', 'owner', 'name',
                  'description', 'image', 'assigned_by',
                  'assignee', 'status', 'start', 'due',]


class LearningTaskViewSet(SendEmailViewMixin, viewsets.ModelViewSet):
    queryset = LearningTask.objects.all()
    serializer_class = LearningTaskSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrIsAnEmployee, )
    filter_class = LearningTaskFilter

    def perform_create(self, serializer):
        """Override the creation function to include creation of associated models."""
        # Create 'Task' models.
        task = serializer.save(
            owner=self.request.user,
            assigned_by=self.request.tenant_me,
            assignee=self.request.tenant_me,
            status=constants.ASSIGNED_TASK_STATUS,
        )

        # Send email notification for 'SortedLogEventByCreated' model.
        # self.send_notification(task, log_event)
