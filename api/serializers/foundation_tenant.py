from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from smegurus import constants
from foundation_tenant.models.governmentbenefitoption import GovernmentBenefitOption
from foundation_tenant.models.identifyoption import IdentifyOption
from foundation_tenant.models.countryoption import CountryOption
from foundation_tenant.models.provinceoption import ProvinceOption
from foundation_tenant.models.cityoption import CityOption
from foundation_tenant.models.fileupload import TenantFileUpload
from foundation_tenant.models.imageupload import TenantImageUpload
from foundation_tenant.models.naicsoption import NAICSOption
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
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.note import Note
from foundation_tenant.models.logevent import SortedLogEventByCreated
from foundation_tenant.models.commentpost import SortedCommentPostByCreated
from foundation_tenant.models.task import Task
from foundation_tenant.models.visitor import TenantVisitor


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


class CountryOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryOption
        fields = ('id', 'name',)


class ProvinceOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvinceOption
        fields = ('id', 'name', 'country',)


class CityOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityOption
        fields = ('id', 'name', 'country', 'province',)


class PostalAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalAddress
        fields = ('id', 'name', 'alternate_name', 'description', 'owner', 'url',
                 'address_country', 'address_locality', 'address_region',
                 'post_office_box_number', 'postal_code', 'street_address',)

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
                  'family_name', 'email', 'telephone', 'has_logout_dialog',)


class CalendarEventSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(read_only=True)
    class Meta:
        model = CalendarEvent
        fields = ('id', 'name', 'description', 'colour', 'start', 'finish', 'participants', 'status',)


class IntakeSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(read_only=True)
    is_employee_created = serializers.BooleanField(read_only=True)
    class Meta:
        model = Intake
        fields = ('id', 'created', 'last_modified', 'me', 'status',
                  'how_can_we_help', 'how_can_we_help_other', 'how_can_we_help_tag',
                  'how_did_you_hear', 'how_did_you_hear_other', 'do_you_own_a_biz',
                  'do_you_own_a_biz_other', 'has_telephone', 'telephone',
                  'telephone_time', 'is_employee_created', 'judgement_note',
                  'government_benefits', 'other_government_benefit',
                  'identities', 'date_of_birth', 'naics_depth_one', 'naics_depth_two',
                  'naics_depth_three', 'naics_depth_four', 'naics_depth_five',
                  'has_signed_privacy_and_terms', 'has_signed_confidentiality_agreement',
                  'has_signed_collection_and_use_of_information', 'has_signed_with_name',
                  'has_signed_on_date', 'privacy_note', 'terms_note', 'confidentiality_note',
                  'collection_note')


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
                  'start', 'due', 'comment_posts', 'log_events', 'type_of',
                  'has_review_requirement', 'download', 'upload', 'calendar_event',)

class SortedLogEventByCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SortedLogEventByCreated
        fields = ('id', 'created', 'last_modified', 'me', 'text',)


class SortedCommentPostByCreatedSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(source='image.imagefile.url', read_only=True)
    class Meta:
        model = SortedCommentPostByCreated
        fields = ('id', 'created', 'last_modified', 'owner', 'name',
                  'description', 'image', 'image_url', 'me',)


class GovernmentBenefitOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentBenefitOption
        fields = ('id', 'order_number', 'name',)


class IdentifyOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentifyOption
        fields = ('id', 'order_number', 'name',)


class NAICSOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NAICSOption
        fields = ('id', 'seq_num', 'name', 'parent', 'year')
