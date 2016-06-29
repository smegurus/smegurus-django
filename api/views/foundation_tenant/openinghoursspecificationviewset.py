import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers.foundation_tenant import OpeningHoursSpecificationSerializer
from foundation_tenant.models.openinghoursspecification import OpeningHoursSpecification


class OpeningHoursSpecificationFilter(django_filters.FilterSet):
    class Meta:
        model = OpeningHoursSpecification
        fields = ['id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'closes', 'day_of_week', 'opens', 'valid_from', 'valid_through',]


class OpeningHoursSpecificationViewSet(viewsets.ModelViewSet):
    queryset = OpeningHoursSpecification.objects.all()
    serializer_class = OpeningHoursSpecificationSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    filter_class = OpeningHoursSpecificationFilter
