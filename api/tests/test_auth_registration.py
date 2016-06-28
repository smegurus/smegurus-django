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
from api.views import authentication


from django.core.urlresolvers import resolve, reverse
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIRegistrationTestCase(APITestCase, TenantTestCase):
    fixtures = [
        # 'banned_domains.json',
        # 'banned_ips.json',
        # 'banned_words.json',
        # 'groups',
        # 'permissions',
    ]

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(  # Create our user.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English
        super(APIRegistrationTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()

    @transaction.atomic
    def test_api_registration_with_success(self):
        # Remove the existing user(s) before continuing.
        self.assertEqual(User.objects.count(), 1)
        for user in User.objects.all():
            user.delete()
        self.assertEqual(User.objects.count(), 0)

        # Beging this unit test.
        url = reverse('api_register')
        data = {
            'username': 'whalesquid@hideauze.com',
            'email': 'whalesquid@hideauze.com',
            'password': 'test',
            'first_name': 'Transhumanist',
            'last_name': '#1'
        }
        response = self.c.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'whalesquid@hideauze.com')

    @transaction.atomic
    def test_api_registration_with_failure(self):
        self.assertEqual(User.objects.count(), 1)
        url = reverse('api_register')
        data = {
            'username': TEST_USER_USERNAME,
            'email': TEST_USER_EMAIL,
            'password': TEST_USER_PASSWORD,
            'first_name': 'Ledo',
            'last_name': 'Clone #123'
        }
        response = self.c.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, TEST_USER_EMAIL)
