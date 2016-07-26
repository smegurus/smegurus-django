import django_filters
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import status
from rest_framework import response
from rest_framework.decorators import detail_route
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrIsAnEmployee, IsOwner
from api.serializers.foundation_tenant  import IntakeSerializer
from foundation_tenant.models.intake import Intake
from foundation_public import constants
from smegurus.settings import env_var


class SendEmailViewMixin(object):
    def login_url(self, schema_name):
        """Function will return the URL to the login page through the sub-domain of the organization."""
        url = 'https://' if self.request.is_secure() else 'http://'
        url += schema_name + "."
        url += get_current_site(self.request).domain
        url += "/en/login/"
        return url

    def send_activation(self, schema_name, contact_list):
        """Function will send to the inputted email the URL that needs to be accessed to activate the account."""
        # contact_list = [env_var('DEFAULT_TO_EMAIL')]
        subject = "New Entrepreneur Application!"
        url = self.login_url(schema_name)
        message = _('A new Entrepreneur has completed the intake application. Login and checkout the new application at: : %(url)s') % {'url': str(url)}

        send_mail(
            subject,
            message,
            env_var('DEFAULT_FROM_EMAIL'),
            contact_list,
            fail_silently=False
        )


class IntakeFilter(django_filters.FilterSet):
    class Meta:
        model = Intake
        fields = ['created', 'last_modified', 'owner', 'is_completed',
                  'how_can_we_help', 'how_can_we_help_other', 'how_can_we_help_tag',
                  'how_did_you_hear', 'how_did_you_hear_other', 'do_you_own_a_biz',
                  'do_you_own_a_biz_other', 'how_to_contact', 'how_to_contact_telephone',
                  'how_to_contact_times',]


class IntakeViewSet(SendEmailViewMixin, viewsets.ModelViewSet):
    queryset = Intake.objects.all()
    serializer_class = IntakeSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrIsAnEmployee, )
    filter_class = IntakeFilter

    @detail_route(methods=['put'], permission_classes=[permissions.IsAuthenticated,])
    def complete_intake(self, request, pk=None):
        try:
            # Attempt to fetch the Object by the unique identifier.
            intake = Intake.objects.get(pk=pk)

            # Security: Only the owner can modify this object.
            if intake.owner != request.user:
                return response.Response(
                    data={'message': 'You are not the owner of this object.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Send a notification to the staff when the Intake was completed.
            # Send a notification to the Organization staff.
            if not intake.is_completed:
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
                self.send_activation(request.tenant.schema_name, contact_list)

                # Mark the Intake object as complete after sending notification.
                intake.is_completed = True
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
