from django.contrib.auth.models import User, Group
from rest_framework import generics, permissions, status, response, views
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from api.serializers import LoginSerializer, TokenSerializer


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
        user = serializer.user
        token, _ = Token.objects.get_or_create(user=user)
        #user_logged_in.send(sender=user.__class__, request=self.request, user=user)
        return response.Response(
            data=TokenSerializer(token).data,
            status=status.HTTP_200_OK,
        )
