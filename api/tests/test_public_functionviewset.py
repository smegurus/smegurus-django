import json
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
from api.views import authentication
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIFunctionViewSetWithPublicSchemaTestCase(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Public Schema"""
        tenant.schema_name = 'test'
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
        translation.activate('en')  # Set English.
        super(APIFunctionViewSetWithPublicSchemaTestCase, self).setUp()

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
        super(APIFunctionViewSetWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_api_function_is_email_unique_with_true(self):
        # Log in the the account.
        user = User.objects.get()
        token = Token.objects.get(user_id=user.id)

        # Begin this unit test.
        url = reverse('api_function_isemailunique')
        data = {
            'email': TEST_USER_EMAIL
        }
        response = self.authorized_client.post(
            url,
            json.dumps(data),
            HTTP_AUTHORIZATION='Token ' + token.key,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'is_unique', response.content)
        self.assertIn(b'false', response.content)

    @transaction.atomic
    def test_api_function_is_email_unique_with_false(self):
        # Log in the the account.
        user = User.objects.get()
        token = Token.objects.get(user_id=user.id)

        # Begin this unit test.
        url = reverse('api_function_isemailunique')
        data = {
            'email': 'Amy@gargantia.com',
        }
        response = self.authorized_client.post(
            url,
            json.dumps(data), HTTP_AUTHORIZATION='Token ' + token.key,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'is_unique', response.content)
        self.assertIn(b'true', response.content)

    @transaction.atomic
    def test_api_function_is_email_unique_with_400(self):
        # Log in the the account.
        user = User.objects.get()
        token = Token.objects.get(user_id=user.id)

        # Begin this unit test.
        url = reverse('api_function_isemailunique')
        data = {
            'password': 'ILoveGAH',
        }
        response = self.authorized_client.post(
            url,
            json.dumps(data), HTTP_AUTHORIZATION='Token ' + token.key,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'email', response.content)
        self.assertIn(b'This field is required.', response.content)

    @transaction.atomic
    def test_api_function_is_email_unique_with_401(self):
        # Begin this unit test.
        url = reverse('api_function_isemailunique')
        data = {
            'email': TEST_USER_EMAIL
        }
        response = self.unauthorized_client.post(url, json.dumps(data), HTTP_AUTHORIZATION='Token 123', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
