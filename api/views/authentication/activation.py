from django.contrib.auth.models import User
from rest_framework import status, response, views
from rest_framework.permissions import AllowAny
from api.serializers import ActivationSerializer


class ActionViewMixin(object):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data) # Activation: Step 1
        if serializer.is_valid():
            return self.action(serializer) # Activation: Step 4 - Success
        else:
            return response.Response( # Activation: Step 4 - Failure
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class ActivationView(ActionViewMixin, views.APIView):
    serializer_class = ActivationSerializer
    permission_classes = [AllowAny,]

    def action(self, serializer):
        serializer.user.is_active = True
        serializer.user.save()
        return response.Response(
            data={},
            status=status.HTTP_200_OK
        )
