import json
from django.db import transaction
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from api.views import authentication
from foundation_tenant.models.postaladdress import PostalAddress
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIPublicPostalAdressWithPublicSchemaTestCase(APITestCase, TenantTestCase):
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
        user = User.objects.create_user(  # Create our user.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English.
        super(APIPublicPostalAdressWithPublicSchemaTestCase, self).setUp()

        # Initialize our test data.
        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)

        # Setup.
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)

        # Above taken from:
        # http://www.django-rest-framework.org/api-guide/testing/#authenticating

        # Initialize our test data.
        PostalAddress.objects.bulk_create([
            PostalAddress(owner=self.user),
            PostalAddress(owner=self.user),
            PostalAddress(owner=self.user),
        ])

    @transaction.atomic
    def tearDown(self):
        postal_addesses = PostalAddress.objects.all()
        for postal_address in postal_addesses.all():
            postal_address.delete()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(APIPublicPostalAdressWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_to_string(self):
        # Create a new object with our specific test data.
        postal_address = PostalAddress.objects.create(
            id=2030,
            name="Unit Test",
            description="Used for unit testing purposes."
        )
        postal_address.save()
        self.assertEqual(str(postal_address), "Unit Test")

    @transaction.atomic
    def test_list(self):
        response = self.unauthorized_client.get(reverse('publicpostaladdress-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_authentication(self):
        response = self.authorized_client.get(reverse('publicpostaladdress-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_post(self):
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'address_country': 'Canada',
            'address_region': 'Ontario',
        }
        response = self.unauthorized_client.post(
            reverse('publicpostaladdress-list'),
            json.dumps(data),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_post_with_authentication(self):
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'address_country': 'Canada',
            'address_region': 'Ontario',
        }
        response = self.authorized_client.post(
            reverse('publicpostaladdress-list'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_post_with_authentication_but_wrong_us_state(self):
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'address_country': 'United States',
            'address_region': 'Ontario',
        }
        response = self.authorized_client.post(
            reverse('publicpostaladdress-list'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_post_with_authentication_but_wrong_ca_state(self):
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'address_country': 'Canada',
            'address_region': 'New York',
        }
        response = self.authorized_client.post(
            reverse('publicpostaladdress-list'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_post_with_authentication_but_wrong_mx_state(self):
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'address_country': 'Mexico',
            'address_region': 'New York',
        }
        response = self.authorized_client.post(
            reverse('publicpostaladdress-list'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_post_with_authentication_but_wrong_cn_state(self):
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'address_country': 'China',
            'address_region': 'New York',
        }
        response = self.authorized_client.post(
            reverse('publicpostaladdress-list'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_post_with_authentication_but_wrong_br_state(self):
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'address_country': 'Brazil',
            'address_region': 'New York',
        }
        response = self.authorized_client.post(
            reverse('publicpostaladdress-list'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_post_with_authentication_but_wrong_ru_state(self):
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'address_country': 'Russia',
            'address_region': 'New York',
        }
        response = self.authorized_client.post(
            reverse('publicpostaladdress-list'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_put(self):
        # Delete any previous data.
        postal_addesses = PostalAddress.objects.all()
        for postal_address in postal_addesses.all():
            postal_addesses.delete()

        # Create a new object with our specific test data.
        PostalAddress.objects.create(
            id=1,
            name="Unit Test",
            description="Used for unit testing purposes."
        )

        # Run the test.
        data = {
            'id': 1,
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'address_country': 'Canada',
            'address_region': 'Ontario',
        }
        response = self.unauthorized_client.put(
            '/api/publicpostaladdress/1/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_put_with_authorization(self):
        # Delete any previous data.
        postal_addesses = PostalAddress.objects.all()
        for postal_address in postal_addesses.all():
            postal_addesses.delete()

        # Create a new object with our specific test data.
        PostalAddress.objects.create(
            id=1,
            name="Unit Test",
            description="Used for unit testing purposes.",
            owner_id=self.user.id
        )

        # Run the test.
        data = {
            'id': 1,
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'address_country': 'Canada',
            'address_region': 'Ontario',
        }
        response = self.authorized_client.put(
            '/api/publicpostaladdress/1/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_delete(self):
        response = self.unauthorized_client.delete('/api/publicpostaladdress/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_with_authentication(self):
        response = self.authorized_client.delete('/api/publicpostaladdress/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
