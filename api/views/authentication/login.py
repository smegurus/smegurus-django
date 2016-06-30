from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions, status, response, views
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from api.serializers.authentication import LoginSerializer, TokenSerializer


class ActionViewMixin(object):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return self.action(serializer)
        else:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginViewSet(ActionViewMixin, views.APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny,]

    def action(self, serializer):
        # Generate our tokens which we will return later.
        user = serializer.user
        token, _ = Token.objects.get_or_create(user=user)

        # Create a session for this User by logging this user in.
        authenticated_user = authenticate(
            username=serializer['username'].value,
            password=serializer['password'].value
        )
        login(self.request, authenticated_user)

        # Return our Token data which will be used throughout our application
        # as the key in our API.
        return response.Response(
            data=TokenSerializer(token).data,
            status=status.HTTP_200_OK,
        )
