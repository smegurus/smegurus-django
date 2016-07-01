import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers.foundation_public import PublicOpeningHoursSpecificationSerializer
from foundation_public.models.openinghoursspecification import PublicOpeningHoursSpecification


class PublicOpeningHoursSpecificationFilter(django_filters.FilterSet):
    class Meta:
        model = PublicOpeningHoursSpecification
        fields = ['id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'closes', 'day_of_week', 'opens', 'valid_from', 'valid_through',]


class PublicOpeningHoursSpecificationViewSet(viewsets.ModelViewSet):
    queryset = PublicOpeningHoursSpecification.objects.all()
    serializer_class = PublicOpeningHoursSpecificationSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    filter_class = PublicOpeningHoursSpecificationFilter
