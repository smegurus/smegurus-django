from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from smegurus import constants
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
from foundation_tenant.models.tellusyourneed import TellUsYourNeed
from foundation_tenant.models.calendarevent import CalendarEvent
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.admission import Admission
from foundation_tenant.models.faqitem import FAQItem
from foundation_tenant.models.faqgroup import FAQGroup
from foundation_tenant.models.communitypost import CommunityPost
from foundation_tenant.models.communityadvertisement import CommunityAdvertisement
from foundation_tenant.models.message import Message
from foundation_tenant.models.note import Note
from foundation_tenant.models.task import Task
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.orderedlogevent import OrderedLogEvent
from foundation_tenant.models.orderedcommentpost import OrderedCommentPost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups')


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

    def validate(self, data):
        """
        Perform our own custom validation.
        """
        address_country = data.get('address_country')
        address_region = data.get('address_region')
        message = _("Province/State does not exist for specified Country.")

        if address_country == _("United States"):
            if not address_region in constants.US_ADDRESS_REGIONS:
                raise serializers.ValidationError(message)

        if address_country == _("Canada"):
            if not address_region in constants.CA_ADDRESS_REGIONS:
                raise serializers.ValidationError(message)

        if address_country == _("Mexico"):
            if not address_region in constants.MX_ADDRESS_REGIONS:
                raise serializers.ValidationError(message)

        if address_country == _("China"):
            if not address_region in constants.CN_ADDRESS_REGIONS:
                raise serializers.ValidationError(message)

        if address_country == _("Brazil"):
            if not address_region in constants.BR_ADDRESS_REGIONS:
                raise serializers.ValidationError(message)

        if address_country == _("Russia"):
            if not address_region in constants.RU_ADDRESS_REGIONS:
                raise serializers.ValidationError(message)

        return super(PostalAddressSerializer, self).validate(data)


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


class TellUsYourNeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TellUsYourNeed
        fields = ('id', 'owner', 'needs_financial_management', 'needs_sales', 'needs_social_media', 'needs_other', 'other',)


class TenantMeSerializer(serializers.ModelSerializer):
    is_admitted = serializers.BooleanField(read_only=True)
    class Meta:
        model = TenantMe
        fields = ('id', 'owner', 'is_admitted', 'tags', 'image', 'description',
                  'url', 'telephone', 'is_tos_signed',
                  'is_setup', 'is_locked', 'notify_when_task_had_an_interaction',
                  'notify_when_new_messages', 'notify_when_due_tasks',
                  'address', 'address', 'contact_point', 'given_name',
                  'family_name', 'email', 'telephone',)


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = ('id', 'name', 'colour', 'start', 'finish',)


class IntakeSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(read_only=True)
    is_employee_created = serializers.BooleanField(read_only=True)
    class Meta:
        model = Intake
        fields = ('id', 'created', 'last_modified', 'me', 'status',
                  'how_can_we_help', 'how_can_we_help_other', 'how_can_we_help_tag',
                  'how_did_you_hear', 'how_did_you_hear_other', 'do_you_own_a_biz',
                  'do_you_own_a_biz_other', 'how_to_contact', 'how_to_contact_telephone',
                  'how_to_contact_times', 'is_employee_created', 'note',)


class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = ('id', 'owner',)


class FAQGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQGroup
        fields = ('id', 'created', 'last_modified', 'text', 'items',)


class FAQItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQItem
        fields = ('id', 'created', 'last_modified', 'question_text',
                  'answer_text', 'likers', 'dislikers',)


class CommunityPostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, required=False, read_only=True)
    me = TenantMeSerializer(many=False, required=False, read_only=True)
    image_url = serializers.URLField(source='image.imagefile.url', read_only=True)
    class Meta:
        model = CommunityPost
        fields = ('id', 'created', 'last_modified', 'owner', 'name',
                  'description', 'likers', 'tags', 'me', 'image', 'image_url',)


class CommunityAdvertisementSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, required=False, read_only=True)
    image_url = serializers.URLField(source='image.imagefile.url', read_only=True)
    class Meta:
        model = CommunityAdvertisement
        fields = ('id', 'created', 'last_modified', 'owner', 'name',
                  'description', 'image', 'image_url',)


class MessageSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, required=False, read_only=True)
    sender = TenantMeSerializer(many=False, required=False, read_only=True)
    image_url = serializers.URLField(source='image.imagefile.url', read_only=True)
    participants = TenantMeSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Message
        fields = ('id', 'created', 'last_modified', 'owner', 'name',
                  'description', 'image', 'image_url', 'sender', 'recipient',
                  'date_read', 'date_received', 'date_sent', 'participants',)


class NoteSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, required=False, read_only=True)
    image_url = serializers.URLField(source='image.imagefile.url', read_only=True)
    class Meta:
        model = Note
        fields = ('id', 'created', 'last_modified', 'owner', 'name',
                  'description', 'image', 'image_url', 'me',)


class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, required=False, read_only=True)
    image_url = serializers.URLField(source='image.imagefile.url', read_only=True)
    class Meta:
        model = Task
        fields = ('id', 'created', 'last_modified', 'owner', 'name',
                  'description', 'image', 'image_url', 'assigned_by',
                  'assignee', 'status', 'participants', 'tags',
                  'start', 'due', 'comment_posts', 'log_events',)

class OrderedLogEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedLogEvent
        fields = ('id', 'created', 'last_modified', 'me', 'text',)


class OrderedCommentPostSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(source='image.imagefile.url', read_only=True)
    class Meta:
        model = OrderedCommentPost
        fields = ('id', 'created', 'last_modified', 'owner', 'name',
                  'description', 'image', 'image_url', 'me',)
