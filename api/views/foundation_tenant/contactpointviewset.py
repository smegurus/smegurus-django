import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import IsOwnerOrIsAnEmployee
from api.serializers.foundation_tenant  import ContactPointSerializer
from foundation_tenant.models.base.contactpoint import ContactPoint


class ContactPointFilter(django_filters.FilterSet):
    class Meta:
        model = ContactPoint
        fields = ['name', 'alternate_name', 'description', 'area_served', 'available_language', 'contact_type', 'email', 'fax_number', 'hours_available', 'product_supported', 'telephone', 'owner']


class ContactPointViewSet(viewsets.ModelViewSet):
    queryset = ContactPoint.objects.all()
    serializer_class = ContactPointSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrIsAnEmployee, )
    filter_class = ContactPointFilter
