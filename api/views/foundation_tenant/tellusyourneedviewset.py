import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.serializers.foundation_tenant  import TellUsYourNeedSerializer
from foundation_tenant.models.tellusyourneed import TellUsYourNeed


class TellUsYourNeedFilter(django_filters.FilterSet):
    class Meta:
        model = TellUsYourNeed
        fields = ['owner', 'needs_financial_management', 'needs_sales', 'needs_social_media', 'needs_other', 'other',]


class TellUsYourNeedViewSet(viewsets.ModelViewSet):
    queryset = TellUsYourNeed.objects.all()
    serializer_class = TellUsYourNeedSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,  )
    filter_class = TellUsYourNeedFilter
