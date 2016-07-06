from django.core.urlresolvers import resolve, reverse
from django.db import transaction
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIActivationTestCase(APITestCase, TenantTestCase):
    fixtures = [
        # 'banned_domains.json',
        # 'banned_ips.json',
        # 'banned_words.json',
        # 'groups',
        # 'permissions',
    ]

    def setup_tenant(self, tenant):
        """Public Schema"""
        tenant.schema_name = 'test'
        tenant.name = "Galactic Alliance of Humankind"

    @classmethod
    def setUpTestData(cls):
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
        super(APIActivationTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(APIActivationTestCase, self).tearDown()

    @transaction.atomic
    def test_api_activation_with_authentication_success(self):
        user = User.objects.get()
        self.assertIsNotNone(user)
        user.is_active = False
        user.save()
        token = Token.objects.get(user_id=user.id)

        # Activate the user.
        url = reverse('api_activate')
        data = {
            'uid': user.id,
            'token': str(token),
        }
        response = self.c.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_api_activation_with_stale_token(self):
        user = User.objects.get()
        self.assertIsNotNone(user)
        token = Token.objects.get(user_id=user.id)

        # Activate the user to generate a "Stale Token" error.
        url = reverse('api_activate')
        data = {
            'uid': user.id,
            'token': str(token),
        }
        response = self.c.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def test_api_activation_with_invalid_uid(self):
        # Activate the user to generate a "Stale Token" error.
        url = reverse('api_activate')
        data = {
            'uid': 666,
            'token': '',
        }
        response = self.c.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_api_activation_with_invalid_token_1(self):
        # Get the user.
        user = User.objects.get()

        # Activate the user to generate a "Stale Token" error.
        url = reverse('api_activate')
        data = {
            'uid': user.id,
            'token': '666',
        }
        response = self.c.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_api_activation_with_invalid_token_2(self):
        user = User.objects.get()
        user.is_active = False
        user.save()
        token = Token.objects.get(user_id=user.id)

        # Activate the user.
        url = reverse('api_activate')
        data = {
            'uid': user.id,
            'token': str(token),
        }

        # Important: By deleting the token, we are will testing to see
        #            how the system will re-act.
        token.delete()
        response = self.c.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
