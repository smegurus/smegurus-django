from django.contrib.auth.models import User
from rest_framework import generics, permissions, status, response, views, filters, mixins
from rest_framework.permissions import AllowAny
from api.serializers import RegisterSerializer


class RegisterViewSet(generics.ListCreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny,]
    queryset = User.objects.none() # Restrict so no-one sees the users.

    def perform_create(self, serializer):
        instance = serializer.save()  # Register: Step 1
        assert instance
