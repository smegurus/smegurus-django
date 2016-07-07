from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from foundation_public.models.imageupload import PublicImageUpload
from foundation_public.models.fileupload import PublicFileUpload
from foundation_public.models.language import PublicLanguage
from foundation_public.models.postaladdress import PublicPostalAddress
from foundation_public.models.openinghoursspecification import PublicOpeningHoursSpecification
from foundation_public.models.contactpoint import PublicContactPoint
from foundation_public.models.geocoordinate import PublicGeoCoordinate
from foundation_public.models.brand import PublicBrand
from foundation_public.models.place import PublicPlace
from foundation_public.models.country import PublicCountry
from foundation_public.models.organization import PublicOrganization
from foundation_public.models.me import PublicMe


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class PublicOrganizationSerializer(serializers.ModelSerializer):
    schema_name = serializers.CharField(required=True)
    class Meta:
        model = PublicOrganization
        fields = ('id', 'created', 'last_modified', 'owner', 'on_trial', 'paid_until', 'name', 'schema_name', 'address', 'brands',
         'contact_point', 'department', 'dissolution_date', 'duns', 'email', 'fax_number', 'founding_date', 'founding_location',
         'global_location_number', 'isic_v4', 'legal_name', 'logo', 'naics', 'parent_organization', 'tax_id', 'telephone', 'vat_id',
         'how_many_served', 'is_tos_signed', 'twitter_url', 'facebook_url', 'instagram_url', 'linkedin_url', 'github_url',
         'google_plus_url', 'youtube_url', 'flickr_url', 'pintrest_url', 'reddit_url', 'soundcloud_url')


class PublicImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicImageUpload
        fields = ('id', 'imagefile', 'created', 'last_modified', 'owner',)


class PublicFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicFileUpload
        fields = ('id', 'datafile', 'created', 'last_modified', 'owner',)


class PublicLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicLanguage
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url')


class PublicPostalAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicPostalAddress
        fields = ('id', 'name', 'alternate_name', 'description', 'address_country', 'address_locality', 'address_region', 'post_office_box_number', 'postal_code', 'street_address', 'owner', 'url')


class PublicOpeningHoursSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicOpeningHoursSpecification
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'closes', 'day_of_week', 'opens', 'valid_from', 'valid_through',)


class PublicContactPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicContactPoint
        fields = ('id', 'name', 'alternate_name', 'description', 'area_served', 'available_language', 'contact_type', 'email', 'fax_number', 'hours_available', 'product_supported', 'telephone', 'owner', 'url')


class PublicGeoCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicGeoCoordinate
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'address', 'address_country', 'elevation', 'latitude', 'longitude', 'postal_code',)


class PublicBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicBrand
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url')


class PublicPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicPlace
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'address', 'fax_number', 'geo', 'global_location_number', 'has_map', 'isic_v4', 'logo', 'opening_hours_specification', 'photo', 'telephone',)


class PublicMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicMe
        fields = ('id', 'created', 'last_modified', 'owner', 'url', 'how_discovered', 'is_tos_signed',)


class PublicCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicCountry
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'how_many_served', 'is_tos_signed', 'twitter_url', 'facebook_url',)
