import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers.foundation_public  import PublicLanguageSerializer
from foundation_public.models.language import PublicLanguage


class PublicLanguageFilter(django_filters.FilterSet):
    class Meta:
        model = PublicLanguage
        fields = ['created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url']


class PublicLanguageViewSet(viewsets.ModelViewSet):
    queryset = PublicLanguage.objects.all()
    serializer_class = PublicLanguageSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAdminUserOrReadOnly, )
    filter_class = PublicLanguageFilter
