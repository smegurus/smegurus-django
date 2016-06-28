import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers  import LanguageSerializer
from api.models.language import Language


class LanguageFilter(django_filters.FilterSet):
    class Meta:
        model = Language
        fields = ['created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url']


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_class = LanguageFilter
