from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from foundation_public.models.banned import BannedDomain
from foundation_public.utils import get_unique_username_from_email

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

    def validate_email(self, value):
        try:
            # Defensive Code 1: Prevent duplicate emails.
            User.objects.get(email=value)
        except User.DoesNotExist:
            # Defensive Code 2: Prevent using banned domains.
            banned_domains = BannedDomain.objects.all()
            for banned_domain in banned_domains.all():
                if str(banned_domain) in value:
                    raise serializers.ValidationError('Email domain is banned.')

            return value
        raise serializers.ValidationError('Email already exists.')

    def validate(self, data):
        """
        Source: http://stackoverflow.com/a/36419160
        """
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)
        password = data.get('password') # get the password from the data

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(RegisterSerializer, self).validate(data)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Create the user account.
        email = validated_data['email']

        # Generate a unique username from the inputted email.
        user.username = get_unique_username_from_email(email)

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


class ChangePasswordSerializer(UidAndTokenSerializer):
    password = serializers.CharField()

    default_error_messages = {
        'inactive_account': INACTIVE_ACCOUNT_ERROR,
    }

    def validate(self, attrs):
        attrs = super(ChangePasswordSerializer, self).validate(attrs)
        if not self.user.is_active:
            raise exceptions.PermissionDenied(self.error_messages['inactive_account'])
        return attrs
