import django_filters
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import authentication
from api.pagination import LargeResultsSetPagination
from api.permissions import ManagementOrAuthenticatedReadOnlyPermission
from api.serializers.foundation_tenant  import IntakeSerializer
from foundation_tenant.models.intake import Intake


class IntakeFilter(django_filters.FilterSet):
    class Meta:
        model = Intake
        fields = ['created', 'last_modified', 'owner', 'is_completed',
                  'how_can_we_help', 'how_can_we_help_other', 'how_can_we_help_tag',
                  'how_did_you_hear', 'how_did_you_hear_other', 'do_you_own_a_biz',
                  'do_you_own_a_biz_other', 'how_to_contact', 'how_to_contact_telephone',
                  'how_to_contact_times',]


class IntakeViewSet(viewsets.ModelViewSet):
    queryset = Intake.objects.all()
    serializer_class = IntakeSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, ManagementOrAuthenticatedReadOnlyPermission, )
    filter_class = IntakeFilter
