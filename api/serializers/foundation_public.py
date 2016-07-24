from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from foundation_public.models.banned import BannedDomain, BannedWord
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
    is_locked = serializers.CharField(read_only=True)
    class Meta:
        model = PublicMe
        fields = ('id', 'created', 'last_modified', 'owner', 'image', 'name',
                 'description', 'url', 'telephone', 'how_discovered',
                 'is_tos_signed', 'is_setup', 'is_locked',
                 'notify_when_new_tasks', 'notify_when_new_messages',
                 'notify_when_due_tasks',)


class PublicCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicCountry
        fields = ('id', 'created', 'last_modified', 'owner', 'name',
                  'alternate_name', 'description', 'url', 'how_many_served',
                  'is_tos_signed', 'twitter_url', 'facebook_url',)


class PublicOrganizationSerializer(serializers.ModelSerializer):
    schema_name = serializers.CharField(required=True)
    owner = UserSerializer(many=False, required=False, read_only=False)
    address = PublicPostalAddressSerializer(many=False, required=False, read_only=False)

    class Meta:
        model = PublicOrganization
        fields = ('id', 'created', 'last_modified', 'owner', 'url', 'on_trial',
                  'paid_until', 'name', 'schema_name', 'address', 'brands',
                  'contact_point', 'dissolution_date', 'duns', 'email',
                  'fax_number', 'founding_date', 'founding_location',
                  'global_location_number', 'isic_v4', 'legal_name', 'logo',
                  'naics', 'tax_id', 'telephone', 'vat_id', 'how_many_served',
                  'is_tos_signed', 'twitter_url', 'facebook_url', 'instagram_url',
                   'linkedin_url', 'github_url', 'google_plus_url', 'youtube_url',
                   'flickr_url', 'pintrest_url', 'reddit_url', 'soundcloud_url',
                   'is_setup', 'learning_preference', 'challenge', 'has_mentors',
                   'has_perks', )

    def validate(self, data):
        """
        Perform our own custom validation.
        """
        schema_name = data.get('schema_name')

        # Validate to ensure there are not capitals.
        if not schema_name.islower():
            raise serializers.ValidationError("Your subdomain can only contain lowercase letters.")

        # Validate to ensure there are no special characters (including whitespace).
        if not schema_name.isalpha():
            raise serializers.ValidationError("Your subdomain cannot have special characters.")

        # Validate to ensure the user doesn't take a valuable sub-domain name
        # that we (ComicsCantina) can use in the future.
        reserved_words = [
            'dev','develop', 'development', 'developments', 'developer',
            'qa','quality', 'qualityassurance', 'developments', 'book', 'books',
            'prod','production', 'productions', 'shop', 'shops', 'docgen',
            'img', 'image', 'images', 'shopping', 'comicbooks', 'comicbook',
            'help', 'contact', 'contactus', 'exchange', 'stock', 'product',
            'products', 'list', 'listing', 'listings', 'directory', 'tech',
            'technology', 'engineer', 'engineering', 'landpage', 'page', 'test',
            'tests', 'testing', 'doc', 'docs', 'document', 'documents',
            'file', 'files', 'ftp', 'sftp', 'server', 'client', 'comic',
            'comics', 'issue', 'issues', 'series', 'publisher', 'publishers',
            'brand', 'brands', 'inv', 'inventory', 'inventorying', 'catalog',
            'inventorys', 'catalogs', 'ios','android','microsoft', 'apple',
            'samsung', 'mobile', 'tablet', '', 'iphone', 'reader', 'reading',
            'download', 'downloader', 'downloading', 'news', 'blogs', 'www',
            'tutorial', 'tutorials', 'edu', 'education', 'educational', 'link',
            'article', 'www2', 'ww3', 'ww4', 'store', 'storing', 'start',
            'begin', 'checkout', 'pos', 'api', 'ssh', 'buy', 'learn',
            'discover', 'discovery',
        ]
        if schema_name in reserved_words:
            raise serializers.ValidationError("Cannot us a reserved word!")

        # Validate to ensure the domain name isn't using a 'bad word'.
        bad_words = BannedWord.objects.all()
        for bad_word in bad_words.all():
            if str(bad_word) in schema_name:
                raise serializers.ValidationError("Cannot us a banned word!")

        return super(PublicOrganizationSerializer, self).validate(data)
