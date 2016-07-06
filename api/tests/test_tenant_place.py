import json
from django.db import transaction
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_tenant.models.place import Place


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIPlaceWithTenantSchemaTestCase(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galacticalliance'
        tenant.name = "Galactic Alliance of Humankind"

    @classmethod
    def setUpTestData(cls):
        # Initialize our test user.
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
        super(APIPlaceWithTenantSchemaTestCase, self).setUp()

        # Initialize our test data.
        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)

        # Setup.
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)

        # Above taken from:
        # http://www.django-rest-framework.org/api-guide/testing/#authenticating

        # Initialize our test data.
        Place.objects.bulk_create([
            Place(owner=self.user),
            Place(owner=self.user),
            Place(owner=self.user),
        ])

    @transaction.atomic
    def tearDown(self):
        places = Place.objects.all()
        for place in places.all():
            place.delete()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(APIPlaceWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_to_string(self):
        # Create a new object with our specific test data.
        place = Place.objects.create(
            id=2030,
            name="Unit Test",
            description="Used for unit testing purposes."
        )
        place.save()
        self.assertEqual(str(place), "Unit Test")

    @transaction.atomic
    def test_list(self):
        response = self.unauthorized_client.get('/api/tenantplace/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_authentication(self):
        response = self.authorized_client.get('/api/tenantplace/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_post(self):
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }
        response = self.unauthorized_client.post('/api/tenantplace/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_post_with_authentication(self):
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }
        response = self.authorized_client.post('/api/tenantplace/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_put(self):
        # Delete any previous data.
        postal_addesses = Place.objects.all()
        for postal_address in postal_addesses.all():
            postal_addesses.delete()

        # Create a new object with our specific test data.
        Place.objects.create(
            id=1,
            name="Unit Test",
            description="Used for unit testing purposes."
        )

        # Run the test.
        data = {
            'id': 1,
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }
        response = self.unauthorized_client.put('/api/tenantplace/1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_put_with_authorization(self):
        # Delete any previous data.
        postal_addesses = Place.objects.all()
        for postal_address in postal_addesses.all():
            postal_addesses.delete()

        # Create a new object with our specific test data.
        Place.objects.create(
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
            'owner': self.user.id
        }
        response = self.authorized_client.put('/api/tenantplace/1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_delete(self):
        response = self.unauthorized_client.delete('/api/tenantplace/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_with_authentication(self):
        response = self.authorized_client.delete('/api/tenantplace/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
