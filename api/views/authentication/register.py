from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, permissions, status, response, views, filters, mixins
from rest_framework.permissions import AllowAny
from api.serializers.authentication import RegisterSerializer
from foundation_public.models.organization import PublicOrganization
from smegurus.settings import env_var
from smegurus import constants


from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import Signer                 # unique value generator.
from django.core.mail import EmailMultiAlternatives    # Emailer
from django.template.loader import render_to_string    # HTML to TXT


class SendEmailViewMixin(object):
    def get_activation_url(self, user):
        # Convert our User's ID into an encrypted value.
        # Note: https://docs.djangoproject.com/en/dev/topics/signing/
        signer = Signer()
        id_sting = str(user.id).encode()
        value = signer.sign(id_sting)

        # Generate our site's URL.
        url = 'https://' if self.request.is_secure() else 'http://'
        schema_name = self.request.tenant.schema_name
        if schema_name == 'public' or schema_name == 'test':
            url += "www."
        else:
            url += schema_name + "."
        url += get_current_site(self.request).domain
        url += reverse('foundation_auth_user_activation', args=[value,])
        url = url.replace("None","en")
        return url

    def send_org_admin_activation(self, user):
        # Generate the data.
        subject = 'Account Activation - SME Gurus for your Organization'
        param = {
            'user': user,
            'url': self.get_activation_url(user), # Generate our activation URL.
            'web_view_url': reverse('foundation_email_activate'),
        }

        # Plug-in the data into our templates and render the data.
        text_content = render_to_string('foundation_auth/activate_org_admin.txt', param)
        html_content = render_to_string('foundation_auth/activate_org_admin.html', param)

        # Generate our address.
        from_email = env_var('DEFAULT_FROM_EMAIL')
        to = user.email

        # Send the email.
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def send_entrepreneur_activation(self, user):
        # Generate the data.
        subject = 'Account Activation - SME Gurus'
        param = {
            'user': user,
            'url': self.get_activation_url(user), # Generate our activation URL.
            'web_view_url': reverse('foundation_email_activate'),
        }

        # Plug-in the data into our templates and render the data.
        text_content = render_to_string('foundation_auth/activate_entrepreneur.txt', param)
        html_content = render_to_string('foundation_auth/activate_entrepreneur.html', param)

        # Generate our address.
        from_email = env_var('DEFAULT_FROM_EMAIL')
        to = user.email

        # Send the email.
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class RegisterViewSet(SendEmailViewMixin, generics.ListCreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny,]
    queryset = User.objects.none() # Restrict so no-one sees the users.

    def perform_create(self, serializer):
        """
        1. Save User.
        2. Assign User to specific Group based on Tenant.
        3. Assign User to specific PublicOrganization.
        """
        user = serializer.save()  # Save the User model from the serializer.

        # Assign the User to the specific Group depending on whether the
        # User was regisered from the Tenant or on the Public schema.
        group = None
        if self.request.tenant.schema_name == 'public' or self.request.tenant.schema_name == 'test':
            group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
            user.groups.add(group)
            self.send_org_admin_activation(user)  # Send our email.
        else:
            group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
            user.groups.add(group)
            self.request.tenant.users.add(user)
            self.send_entrepreneur_activation(user)  # Send our email.
