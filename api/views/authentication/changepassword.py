from django.core.management import call_command
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status, response, views
from rest_framework.permissions import AllowAny
from api.serializers.authentication import ChangePasswordSerializer
from smegurus.settings import env_var


class ActionViewMixin(object):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            return self.action(serializer)
        else:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ChangePasswordViewSet(ActionViewMixin, views.APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [AllowAny,]

    def action(self, serializer):
        # Fetch the email that the User inputted.
        uid = serializer.data['uid']
        new_password = serializer.data['password']

        # Change to our new User password.
        user = User.objects.get(id=uid)
        user.set_password(new_password)
        user.save()

        # Return success.
        return response.Response(
            data={},
            status=status.HTTP_200_OK,
        )
