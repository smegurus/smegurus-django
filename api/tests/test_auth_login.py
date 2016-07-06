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
from api.views import authentication


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APILoginTestCase(APITestCase, TenantTestCase):
    fixtures = [
        # 'banned_domains.json',
        # 'banned_ips.json',
        # 'banned_words.json',
        # 'groups',
        # 'permissions',
    ]

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
        super(APILoginTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(APILoginTestCase, self).tearDown()

    @transaction.atomic
    def test_api_login_with_success(self):
        url = reverse('api_login')
        data = {
            'username': TEST_USER_USERNAME,
            'password': TEST_USER_PASSWORD,
        }
        response = self.c.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'] > 0, True)
        self.assertEqual(len(response.data['auth_token']) > 0, True)

    @transaction.atomic
    def test_api_login_with_nonexisting_account(self):
        url = reverse('api_login')
        data = {
            'username': 'hideauze',
            'password': 'Evolvers',
        }
        response = self.c.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_api_login_with_inactive_account(self):
        # Get our current user and set the user to be inactive.
        client = User.objects.get()
        client.is_active = False
        client.save()

        # Run this test.
        url = reverse('api_login')
        data = {
            'username': TEST_USER_USERNAME,
            'password': TEST_USER_PASSWORD,
        }
        response = self.c.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
