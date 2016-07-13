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
from foundation_tenant.models.openinghoursspecification import OpeningHoursSpecification
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.geocoordinate import GeoCoordinate
from foundation_tenant.models.country import Country
from foundation_tenant.models.brand import Brand
from foundation_tenant.models.place import Place
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.businessidea import BusinessIdea


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


class OpeningHoursSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHoursSpecification
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'closes', 'day_of_week', 'opens', 'valid_from', 'valid_through',)


class ContactPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPoint
        fields = ('id', 'name', 'alternate_name', 'description', 'area_served', 'available_language', 'contact_type', 'email', 'fax_number', 'hours_available', 'product_supported', 'telephone', 'owner', 'url')


class GeoCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoCoordinate
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'address', 'address_country', 'elevation', 'latitude', 'longitude', 'postal_code',)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url',)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url')


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'address', 'fax_number', 'geo', 'global_location_number', 'has_map', 'isic_v4', 'logo', 'opening_hours_specification', 'photo', 'telephone',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'is_program',)


class BusinessIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessIdea
        fields = ('id', 'name', 'industry', 'image', 'owner',)
