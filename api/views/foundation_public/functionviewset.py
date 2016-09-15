from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, status, response, views
from rest_framework.authtoken.models import Token
from rest_framework import exceptions, serializers
from foundation_public.models.organization import PublicOrganization


class IsEmailUniqueSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=75)


class IsEmailUniqueViewSet(views.APIView):
    """Checks to see if this email is unique"""
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        serializer = IsEmailUniqueSerializer(data=request.data)
        if serializer.is_valid():
            user_count = User.objects.filter(email=serializer.data['email']).count()

            return response.Response(
                data={
                    'is_unique': user_count == 0
                },
                status=status.HTTP_200_OK
            )
        else:
            return response.Response(
                data={
                    'is_unique': False,
                    'message': str(serializer.errors)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class TextSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=75)


class IsOrganizationSchemaNameUniqueViewSet(views.APIView):
    """Checks to see if this Organization 'schema_name' is unique"""
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        serializer = TextSerializer(data=request.data)
        if serializer.is_valid():
            count = PublicOrganization.objects.filter(schema_name=serializer.data['name']).count()
            return response.Response(
                data={
                    'is_unique': count == 0
                },
                status=status.HTTP_200_OK
            )
        else:
            return response.Response(
                data={
                    'is_unique': False,
                    'message': str(serializer.errors)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
