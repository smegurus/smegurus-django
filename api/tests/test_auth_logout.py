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
from api.views import authentication


from django.core.urlresolvers import resolve, reverse
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APILogoutTestCase(APITestCase, TenantTestCase):
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
        super(APILogoutTestCase, self).setUp()

        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key, format='json',)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        tokens = Token.objects.all()

    @transaction.atomic
    def test_api_logout_with_success(self):
        # Log in the the account.
        user = User.objects.get()
        token = Token.objects.get(user_id=user.id)

        # Begin this unit test.
        url = reverse('api_logout')
        data = {}
        response = self.authorized_client.post(url, json.dumps(data), HTTP_AUTHORIZATION='Token ' + token.key, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_api_logout_with_failure(self):
        # Begin this unit test.
        url = reverse('api_logout')
        data = {}
        response = self.unauthorized_client.post(url, json.dumps(data), HTTP_AUTHORIZATION='Token 123', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
