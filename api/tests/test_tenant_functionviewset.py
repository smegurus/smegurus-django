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
from tenant_schemas.test.cases import TenantTestCase
from tenant_schemas.test.client import TenantClient
from api.views import authentication
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIFunctionViewSetWithTenantSchemaTestCase(APITestCase, TenantTestCase):
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
        super(APIFunctionViewSetWithTenantSchemaTestCase, self).setUp()

        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key, format='json',)

    @transaction.atomic
    def tearDown(self):
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        TenantMe.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        tokens = Token.objects.all()
        # super(APIFunctionViewSetWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_api_function_finalize_tenant_with_200(self):
        # Log in the the account.
        user = User.objects.get()
        token = Token.objects.get(user_id=user.id)

        # Make User an Employee.
        group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        user.groups.add(group)

        # Begin this unit test.
        url = reverse('api_function_finalize_tenant')
        response = self.authorized_client.post(
            url,
            json.dumps({}),
            HTTP_AUTHORIZATION='Token ' + token.key,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_api_function_finalize_tenant_with_403(self):
        # Log in the the account.
        user = User.objects.get()
        token = Token.objects.get(user_id=user.id)

        # Begin this unit test.
        url = reverse('api_function_finalize_tenant')
        response = self.authorized_client.post(
            url,
            json.dumps({}),
            HTTP_AUTHORIZATION='Token ' + token.key,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def test_api_function_finalize_tenant_with_401(self):
        # Begin this unit test.
        url = reverse('api_function_finalize_tenant')
        response = self.unauthorized_client.post(
            url,
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
