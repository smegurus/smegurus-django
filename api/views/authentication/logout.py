from django.contrib.auth.models import User
from rest_framework import permissions, status, response, views
from rest_framework.authtoken.models import Token


class LogoutViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return response.Response(status=status.HTTP_200_OK)
