from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from foundation_public.models.banned import BannedDomain, BannedWord
from foundation_tenant.models.base.governmentbenefitoption import GovernmentBenefitOption
from foundation_tenant.models.base.identifyoption import IdentifyOption
from foundation_tenant.models.base.countryoption import CountryOption
from foundation_tenant.models.base.provinceoption import ProvinceOption
from foundation_tenant.models.base.cityoption import CityOption
from foundation_tenant.models.base.fileupload import FileUpload
from foundation_tenant.models.base.imageupload import ImageUpload
from foundation_tenant.models.base.naicsoption import NAICSOption
from foundation_tenant.models.base.language import Language
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.openinghoursspecification import OpeningHoursSpecification
from foundation_tenant.models.base.contactpoint import ContactPoint
from foundation_tenant.models.base.geocoordinate import GeoCoordinate
from foundation_tenant.models.base.country import Country
from foundation_tenant.models.base.brand import Brand
from foundation_tenant.models.base.place import Place
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.businessidea import BusinessIdea
from foundation_tenant.models.base.tellusyourneed import TellUsYourNeed
from foundation_tenant.models.base.calendarevent import CalendarEvent
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.admission import Admission
from foundation_tenant.models.base.faqitem import FAQItem
from foundation_tenant.models.base.faqgroup import FAQGroup
from foundation_tenant.models.base.communitypost import CommunityPost
from foundation_tenant.models.base.communityadvertisement import CommunityAdvertisement
from foundation_tenant.models.base.message import Message
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.note import Note
from foundation_tenant.models.base.logevent import SortedLogEventByCreated
from foundation_tenant.models.base.commentpost import SortedCommentPostByCreated
from foundation_tenant.models.base.task import Task
from foundation_tenant.models.base.visitor import Visitor
from foundation_tenant.models.base.inforesourcecategory import InfoResourceCategory
from foundation_tenant.models.base.inforesource import InfoResource
from foundation_tenant.models.base.notification import Notification
from foundation_tenant.utils import int_or_none
from smegurus import constants


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups')


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ('id', 'imagefile', 'created', 'last_modified', 'owner',)


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
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
                  'country', 'postal_code', 'locality', 'region',
                  'street_number', 'suffix',
                  'street_name', 'suite_number',
                  'address_line_2',
                  'address_line_3', 'latitude', 'longitude')

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


class MeSerializer(serializers.ModelSerializer):
    is_in_intake = serializers.BooleanField(read_only=True)
    class Meta:
        model = Me
        fields = ('id', 'owner', 'is_in_intake', 'tags', 'image', 'description',
                  'url', 'telephone', 'is_tos_signed', 'stage_num',
                  'is_setup', 'is_locked', 'notify_when_task_had_an_interaction',
                  'notify_when_new_messages', 'notify_when_due_tasks',
                  'address', 'address', 'contact_point', 'given_name',
                  'family_name', 'email', 'telephone', 'has_logout_dialog',
                  'managed_by', 'gender', 'gender_other', 'level_of_education',
                  'level_of_education_other', 'place_of_birth',
                  'place_of_birth_other', 'employment_status',
                  'employment_status_other', 'education_or_training_status',
                  'education_or_training_status_other', 'why_be_entrepreneur',
                  'why_be_entrepreneur_other', 'challenges_becoming_entrepreneur',
                  'challenges_becoming_entrepreneur_other', 'annual_income_bracket',
                  'has_owned_business', 'has_owned_business_other')


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = ('id', 'name', 'description', 'type_of', 'colour', 'start', 'finish', 'tags', 'pending', 'attendees', 'absentees',)


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
                  'government_benefits', 'other_government_benefit', 'has_business_idea',
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
    me = MeSerializer(many=False, required=False, read_only=True)
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
    sender = MeSerializer(many=False, required=False, read_only=True)
    image_url = serializers.URLField(source='image.imagefile.url', read_only=True)
    participants = MeSerializer(many=True, required=False, read_only=True)
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
                  'description', 'image', 'image_url', 'status', 'type_of',
                  'start', 'is_due', 'due', 'tags', 'assigned_by', 'participants',
                  'opening', 'closures', 'comment_posts', 'log_events', 'uploads',
                  'resources',)


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


class InfoResourceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoResourceCategory
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url',)


class InfoResourceSerializer(serializers.ModelSerializer):
    category_icon = serializers.CharField(read_only=True, source="category.icon")
    category_name = serializers.CharField(read_only=True, source="category.name")
    class Meta:
        model = InfoResource
        fields = ('id', 'created', 'last_modified', 'owner', 'name', 'alternate_name', 'description', 'url', 'is_stock', 'category', 'uploads', 'is_for_staff', 'is_for_entrepreneur', 'stage_num', 'tags', 'category_icon', 'category_name')

    def validate(self, data):
        """
        Perform our own custom validation.
        """
        description = data.get('description')
        name = data.get('name')

        # Validate to ensure the description isn't using a 'bad word'.
        bad_words = BannedWord.objects.all()
        for bad_word in bad_words.all():
            if str(bad_word) in description:
                raise serializers.ValidationError("Cannot us a banned word: "+str(bad_word)+" in description.")
            if str(bad_word) in name:
                raise serializers.ValidationError("Cannot us a banned word: "+str(bad_word)+" in name.")

        return super(InfoResourceSerializer, self).validate(data)


class NotificationSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = Notification
        fields = ('id', 'created', 'last_modified', 'owner', 'name',
                  'description', 'image', 'closures', 'icon', 'type_of')
