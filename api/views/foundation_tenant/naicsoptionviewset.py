import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers.foundation_tenant  import NAICSOptionSerializer
from foundation_tenant.models.naicsoption import NAICSOption


class NAICSOptionFilter(django_filters.FilterSet):
    class Meta:
        model = NAICSOption
        fields = ['id', 'seq_num', 'name', 'parent', 'year']


class NAICSOptionViewSet(viewsets.ModelViewSet):
    queryset = NAICSOption.objects.all()
    serializer_class = NAICSOptionSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsAdminUserOrReadOnly, )
    filter_class = NAICSOptionFilter
