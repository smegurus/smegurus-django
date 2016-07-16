from django.core.management import call_command
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status, response, views
from rest_framework.permissions import AllowAny
from api.serializers.authentication import EmailSerializer
from smegurus.settings import env_var


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


class EmailPasswordResetViewSet(ActionViewMixin, views.APIView):
    serializer_class = EmailSerializer
    permission_classes = [AllowAny,]

    def action(self, serializer):
        # Fetch the email that the User inputted.
        email = serializer.data['email']

        # Send password reset email.
        call_command('send_password_reset_email',str(email))

        return response.Response(
            data={},
            status=status.HTTP_200_OK,
        )
