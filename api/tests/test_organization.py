import json
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


class APIOrganizationTestCase(APITestCase, TenantTestCase):
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
        translation.activate('en')  # Set English.
        super(APIOrganizationTestCase, self).setUp()

        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key, format='json',)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()

    @transaction.atomic
    def test_api_create_tenant_with_success(self):
        # Beging this unit test.
        url = reverse('api_organization')
        data = {
            'schema_name': 'galactic_alliance_of_humankind',
            'name': 'Galactic Alliance of Humankind',
            'paid_until': '2016-12-01',
            'on_trial': True,
        }
        response = self.authorized_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(User.objects.count(), 1)
        # self.assertEqual(User.objects.get().email, 'whalesquid@hideauze.com')
