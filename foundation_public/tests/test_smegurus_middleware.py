import base64
import hashlib
from django.core import mail
from django.core.urlresolvers import resolve, reverse
from django.db import transaction
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from django.core.management import call_command
from foundation_public import constants
from smegurus.settings import env_var


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class SMEGurusTokenMiddlewareWithPublicSchemaTestCase(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Public Schema"""
        tenant.schema_name = 'test'  # Do not change this!
        tenant.name = "Galactic Alliance of Humankind"
        tenant.has_perks=True
        tenant.has_mentors=True
        tenant.how_discovered = "Command HQ"
        tenant.how_many_served = 1

    @classmethod
    def setUpTestData(cls):
        Group.objects.bulk_create([
            Group(id=constants.ENTREPRENEUR_GROUP_ID, name="Entreprenuer",),
            Group(id=constants.MENTOR_GROUP_ID, name="Mentor",),
            Group(id=constants.ADVISOR_GROUP_ID, name="Advisor",),
            Group(id=constants.ORGANIZATION_MANAGER_GROUP_ID, name="Org Manager",),
            Group(id=constants.ORGANIZATION_ADMIN_GROUP_ID, name="Org Admin",),
            Group(id=constants.CLIENT_MANAGER_GROUP_ID, name="Client Manager",),
            Group(id=constants.SYSTEM_ADMIN_GROUP_ID, name="System Admin",),
        ])
        user = User.objects.create_user(  # Create our User.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English
        super(SMEGurusTokenMiddlewareWithPublicSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)
        self.user = User.objects.get()

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        groups = Group.objects.all()
        for group in groups.all():
            group.delete()
        super(SMEGurusTokenMiddlewareWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_token_middleware_with_authentication_with_token(self):
        # Setup
        email = self.user.email.lower()  # Emails should be case-insensitive unique
        converted = email.encode('utf8', 'ignore')  # Deal with internationalized email addresses
        self.user.username = base64.urlsafe_b64encode(hashlib.sha256(converted).digest())[:30]
        self.user.save()

        # Test
        token = Token.objects.get(user__email=TEST_USER_EMAIL)
        authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)
        authenticated_user = authorized_client.login(
            username=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD
        )
        self.assertTrue(authenticated_user)

        response = authorized_client.get(reverse('public_index'))
        self.assertEqual(response.status_code, 200)

    @transaction.atomic
    def test_token_middleware_with_anonymous_user(self):
        response = self.c.get(reverse('public_index'))
        self.assertEqual(response.status_code, 200)

    @transaction.atomic
    def test_token_middleware_with_authentication_without_token(self):
        # Setup
        email = self.user.email.lower()  # Emails should be case-insensitive unique
        converted = email.encode('utf8', 'ignore')  # Deal with internationalized email addresses
        self.user.username = base64.urlsafe_b64encode(hashlib.sha256(converted).digest())[:30]
        self.user.save()

        # Test
        token = Token.objects.get(user__email=TEST_USER_EMAIL)
        authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)
        authenticated_user = authorized_client.login(
            username=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD
        )
        self.assertTrue(authenticated_user)
        token = Token.objects.get(user__email=TEST_USER_EMAIL)
        token.delete()

        response = authorized_client.get(reverse('public_index'))
        self.assertEqual(response.status_code, 200)
