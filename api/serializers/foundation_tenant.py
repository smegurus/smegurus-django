from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from foundation_tenant.models.imageupload import TenantImageUpload
from foundation_tenant.models.fileupload import TenantFileUpload
from foundation_tenant.models.language import Language
from foundation_tenant.models.postaladdress import PostalAddress


class TenantImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantImageUpload
        fields = ('id', 'imagefile', 'created', 'last_modified', 'owner',)


class TenantFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantFileUpload
        fields = ('id', 'datafile', 'created', 'last_modified', 'owner',)


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url')


class PostalAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalAddress
        fields = ('id', 'name', 'alternate_name', 'description', 'address_country', 'address_locality', 'address_region', 'post_office_box_number', 'postal_code', 'street_address', 'owner', 'url')
