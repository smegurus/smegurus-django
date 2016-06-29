from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from foundation.models.public.organization import Organization
from foundation.models.public.imageupload import PublicImageUpload
from foundation.models.public.fileupload import PublicFileUpload
from foundation.models.tenant.imageupload import TenantImageUpload
from foundation.models.tenant.fileupload import TenantFileUpload


class OrganizationSerializer(serializers.ModelSerializer):
    schema_name = serializers.CharField(required=True)
    class Meta:
        model = Organization
        fields = ('id', 'created_on', 'last_modified', 'on_trial',
                  'paid_until', 'name', 'alternate_name', 'description',
                  'image', 'owner', 'schema_name')


class PublicImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicImageUpload
        fields = ('id', 'imagefile', 'created', 'last_modified', 'owner',)


class PublicFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicFileUpload
        fields = ('id', 'datafile', 'created', 'last_modified', 'owner',)


class TenantImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantImageUpload
        fields = ('id', 'imagefile', 'created', 'last_modified', 'owner',)


class TenantFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantFileUpload
        fields = ('id', 'datafile', 'created', 'last_modified', 'owner',)
