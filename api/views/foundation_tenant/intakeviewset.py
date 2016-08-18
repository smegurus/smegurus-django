import django_filters
from django.core.management import call_command
from django.core.mail import EmailMultiAlternatives    # Emailer
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string    # HTML to TXT
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework import response
from rest_framework import exceptions, serializers
from rest_framework.decorators import detail_route
from api.pagination import LargeResultsSetPagination
from api.permissions import IsMeOrIsAnEmployee, IsMe, EmployeePermission
from api.serializers.foundation_tenant  import IntakeSerializer
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.note import Note
from smegurus.settings import env_var
from smegurus import constants


class JudgeIntakeSerializer(serializers.Serializer):
    status = serializers.IntegerField(required=True,)
    comment = serializers.CharField(max_length=2055, required=False,)
    is_employee_created = serializers.BooleanField(default=False, required=False,)


class SendEmailViewMixin(object):
    def get_login_url(self):
        """Function will return the URL to the login page through the sub-domain of the organization."""
        url = 'https://' if self.request.is_secure() else 'http://'
        url += self.request.tenant.schema_name + "."
        url += get_current_site(self.request).domain
        url += reverse('foundation_auth_user_login')
        url = url.replace("None","en")
        return url

    def send_pending_intake(self, contact_list):
        """Function will send pending new intake needs to be reviewed email."""
        # Generate the data.
        subject = "New Entrepreneur Application!"
        param = {
            'url': self.get_login_url(), # Generate our activation URL.
        }

        # Plug-in the data into our templates and render the data.
        text_content = render_to_string('api/email/pending_intake.txt', param)
        html_content = render_to_string('api/email/pending_intake.html', param)

        # Generate our address.
        from_email = env_var('DEFAULT_FROM_EMAIL')

        # Send the email.
        msg = EmailMultiAlternatives(subject, text_content, from_email, contact_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class IntakeFilter(django_filters.FilterSet):
    class Meta:
        model = Intake
        fields = ['created', 'last_modified', 'me', 'status',
                  'how_can_we_help', 'how_can_we_help_other', 'how_can_we_help_tag',
                  'how_did_you_hear', 'how_did_you_hear_other', 'do_you_own_a_biz',
                  'do_you_own_a_biz_other', 'how_to_contact', 'how_to_contact_telephone',
                  'how_to_contact_times',]


class IntakeViewSet(SendEmailViewMixin, viewsets.ModelViewSet):
    queryset = Intake.objects.all()
    serializer_class = IntakeSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, IsMeOrIsAnEmployee, )
    filter_class = IntakeFilter

    def perform_destroy(self, instance):
        """Override the deletion function to archive the message instead of deleting it."""
        # Delete associated models with this model.
        if instance.note:
            instance.note.delete()

        instance.delete()  # Default deletion function.

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated,])
    def complete_intake(self, request, pk=None):
        try:
            # Attempt to fetch the Object by the unique identifier.
            intake = Intake.objects.get(pk=pk)

            # Security: Only the owner can modify this object.
            if intake.me != request.tenant_me:
                return response.Response(
                    data={'message': 'You are not the owner of this object.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Send a notification to the staff when the Intake was completed.
            # Send a notification to the Organization staff.
            if intake.status != constants.PENDING_REVIEW_STATUS:
                # Generate our email list.
                contact_list = []
                users = User.objects.filter(groups__id=constants.ADVISOR_GROUP_ID)
                for user in users.all():
                    contact_list.append(user.email)
                users = User.objects.filter(groups__id=constants.ORGANIZATION_MANAGER_GROUP_ID)
                for user in users.all():
                    contact_list.append(user.email)
                users = User.objects.filter(groups__id=constants.ORGANIZATION_ADMIN_GROUP_ID)
                for user in users.all():
                    contact_list.append(user.email)

                # Send the email to our group.
                self.send_pending_intake(contact_list)

                # Mark the Intake object as complete after sending notification.
                intake.status = constants.PENDING_REVIEW_STATUS
                intake.save()

            # Return a sucess message.
            return response.Response(
                data={'message': 'Intake has been completed.'},
                status=status.HTTP_200_OK
            )
        except Intake.DoesNotExist:
            # Return an error message.
            return response.Response(
                data={'message': 'Pk not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated, EmployeePermission,])
    def judge(self, request, pk=None):
        """
        Function will change the status to either 'Rejected' or 'Accepted' including
        a comment from the employee.
        """
        try:
            serializer = JudgeIntakeSerializer(data=request.data)
            if serializer.is_valid():
                # Updated 'Intake' model.
                intake = self.get_object()
                intake.status = serializer.data['status']
                intake.is_employee_created = serializer.data['is_employee_created']
                intake.save()

                # Update 'Me' model.
                intake.me.is_admitted = (intake.status == constants.APPROVED_STATUS)
                intake.me.save()

                # Update or create 'Note' model.
                description = serializer.data['comment']
                if intake.note:
                    intake.note.name = _("Intake Note")
                    intake.note.description = description
                    intake.note.save()
                else:
                    intake.note = Note.objects.create(
                        me=intake.me,
                        name = _("Intake Note"),
                        description = description,
                    )
                    intake.save()

                # Send the email.
                call_command('send_reviewed_email_for_intake', str(intake.id))

                # Return a success response.
                return response.Response(
                    status=status.HTTP_200_OK
                )
            else:
                return response.Response(
                    data={'message': str(serializer.errors)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return response.Response(
                data={'message': str(e) },
                status=status.HTTP_400_BAD_REQUEST
            )
