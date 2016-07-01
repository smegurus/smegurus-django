import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers.foundation_public  import PublicContactPointSerializer
from foundation_public.models.contactpoint import PublicContactPoint


class PublicContactPointFilter(django_filters.FilterSet):
    class Meta:
        model = PublicContactPoint
        fields = ['name', 'alternate_name', 'description', 'area_served', 'available_language', 'contact_type', 'email', 'fax_number', 'hours_available', 'product_supported', 'telephone', 'owner']


class PublicContactPointViewSet(viewsets.ModelViewSet):
    queryset = PublicContactPoint.objects.all()
    serializer_class = PublicContactPointSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    filter_class = PublicContactPointFilter
