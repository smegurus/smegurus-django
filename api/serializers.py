from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from foundation.models.organization import Organization
from api.models.privateimageupload import PrivateImageUpload
from api.models.privatefileupload import PrivateFileUpload
from api.models.language import Language
from api.models.postaladdress import PostalAddress
from api.models.openinghoursspecification import OpeningHoursSpecification
from api.models.contactpoint import ContactPoint
from api.models.geocoordinate import GeoCoordinate


INVALID_CREDENTIALS_ERROR = _('Unable to login with provided credentials.')
INACTIVE_ACCOUNT_ERROR = _('User account is disabled.')
INVALID_TOKEN_ERROR = _('Invalid token for given user.')
INVALID_UID_ERROR = _('Invalid user id or user doesn\'t exist.')
STALE_TOKEN_ERROR = _('Stale token for given user.')
PASSWORD_MISMATCH_ERROR = _('The two password fields didn\'t match.')
USERNAME_MISMATCH_ERROR = _('The two {0} fields didn\'t match.')
INVALID_PASSWORD_ERROR = _('Invalid password.')
NO_EMAIL_EXISTS_ERROR = _('The entered email does not exist in the system.')


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['auth_token', 'user',]

    auth_token = serializers.CharField(source='key')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
    )

    class Meta:
        model = User
        fields = ('username','email', 'password', 'first_name', 'last_name',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Step 2: Create the user account.

        user.is_active = False  # Lock the account.
        user.save()

        return user  # Return our locked account.


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password')

    default_error_messages = {
        'inactive_account': INACTIVE_ACCOUNT_ERROR,
        'invalid_credentials': INVALID_CREDENTIALS_ERROR,
    }

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.user = None
        self.fields[User.USERNAME_FIELD] = serializers.CharField(required=False)

    def validate(self, attrs):
        self.user = authenticate(
            username=attrs.get(User.USERNAME_FIELD),
            password=attrs.get('password')
        )
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class EmailSerializer(serializers.ModelSerializer):
    """"Serializer used for password resets and account activation."""

    default_error_messages = {
        'no_email': NO_EMAIL_EXISTS_ERROR,
    }

    class Meta:
        model = User
        fields = ('email',)

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError) as error:
            raise serializers.ValidationError(self.error_messages['no_email'])
        return value


class UidAndTokenSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    default_error_messages = {
        'invalid_token': INVALID_TOKEN_ERROR,
        'invalid_uid': INVALID_UID_ERROR,
    }

    def validate_uid(self, value):
        try:
            self.user = User.objects.get(pk=value)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError) as error:
            raise serializers.ValidationError(self.error_messages['invalid_uid'])
        return value

    def validate(self, attrs):
        attrs = super(UidAndTokenSerializer, self).validate(attrs)
        uid = int(attrs['uid'])
        actual_token = attrs['token']

        # Verify the UID returns a Token record.
        try:
            expected_token = Token.objects.get(user_id=uid)
        except Token.DoesNotExist:
            raise serializers.ValidationError(self.error_messages['invalid_token'])

        # Verfiy that the inputted Token matches what we have on record.
        if str(expected_token) != str(actual_token):
            raise serializers.ValidationError(self.error_messages['invalid_token'])

        return attrs


class ActivationSerializer(UidAndTokenSerializer):
    default_error_messages = {
        'stale_token': STALE_TOKEN_ERROR,
    }

    def validate(self, attrs):
        attrs = super(ActivationSerializer, self).validate(attrs)
        if self.user.is_active:
            raise exceptions.PermissionDenied(self.error_messages['stale_token'])
        return attrs


class OrganizationSerializer(serializers.ModelSerializer):
    schema_name = serializers.CharField(required=True)
    class Meta:
        model = Organization
        fields = ('id', 'created_on', 'last_modified', 'on_trial', 'paid_until', 'name', 'schema_name')


class PrivateImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateImageUpload
        fields = ('id', 'imagefile', 'created', 'last_modified', 'owner',)


class PrivateFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateFileUpload
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
