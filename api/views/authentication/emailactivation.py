from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework import status, response, views
from rest_framework.permissions import AllowAny
from api.serializers.authentication import EmailSerializer
from smegurus.settings import env_var


from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class SendEmailViewMixin(object):
    def activation_url(self, email):  #TODO: REMOVE
        """Function will get the User ID and Token and generate a URL."""
        # Fetch the User.
        user = User.objects.get(email=email)
        token = Token.objects.get(user_id=user.id)

        # Developer Notes:
        # Generate the URL in this block of code. Please note the URL links to
        # the link at: "authentication.views.activation_page".
        url = 'https://' if self.request.is_secure() else 'http://'
        url += get_current_site(self.request).domain
        url += "/en/activate/"+str(user.id)+"/"+str(token)+"/"
        return url

    def send_activation(self, email):
        """Function will send to the inputted email the URL that needs to be accessed to activate the account."""
        contact_list = [env_var('DEFAULT_TO_EMAIL')]
        name = "Test Name"
        subject = "Den Activation"
        message = "To activate your account, please click this url: " + self.activation_url(email)  #TODO: Replace w/ resolve_full_url_with_subdmain

        send_mail(
            subject,
            message,
            env_var('DEFAULT_FROM_EMAIL'),
            contact_list,
            fail_silently=False
        )


class ActionViewMixin(object):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            return self.action(serializer)
        else:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class EmailActivationView(SendEmailViewMixin, ActionViewMixin, views.APIView):
    serializer_class = EmailSerializer
    permission_classes = [AllowAny,]

    def action(self, serializer):
        # Fetch the email that the User inputted and send an activation email.
        email = serializer.data['email']
        self.send_activation(email)

        return response.Response(
            data={},
            status=status.HTTP_200_OK,
        )
