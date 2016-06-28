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
from api.views import authentication
from api.models.contactpoint import ContactPoint


from django.core.urlresolvers import resolve, reverse
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIContactPointTestCase(APITestCase, TenantTestCase):
    fixtures = []

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
        super(APIContactPointTestCase, self).setUp()

        # Initialize our test data.
        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)

        # Setup.
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)

        # Initialize our test data.
        ContactPoint.objects.bulk_create([
            ContactPoint(owner=self.user),
            ContactPoint(owner=self.user),
            ContactPoint(owner=self.user),
        ])

        # Above taken from:
        # http://www.django-rest-framework.org/api-guide/testing/#authenticating

    @transaction.atomic
    def tearDown(self):
        contact_points = ContactPoint.objects.all()
        for contact_point in contact_points.all():
            contact_point.delete()

        users = User.objects.all()
        for user in users.all():
            user.delete()

    @transaction.atomic
    def test_to_string(self):
        # Create a new object with our specific test data.
        contact_point = ContactPoint.objects.create(
            id=2030,
            name="Unit Test",
            description="Used for unit testing purposes."
        )
        contact_point.save()
        self.assertEqual(str(contact_point), "Unit Test")

    @transaction.atomic
    def test_list(self):
        # Step 1: Set the location variables.
        url = reverse('contactpoint-list')

        # Step 2: Test & verify.
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_authentication(self):
        # Step 1: Set the location variables.
        url = reverse('contactpoint-list')

        # Step 2: Test & verify.
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_post(self):
        # Step 1: Set the location variables.
        url = reverse('contactpoint-list')
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }

        # Step 2: Test & verify.
        response = self.unauthorized_client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_post_with_authentication(self):
        # Step 1: Set the location variables.
        url = reverse('contactpoint-list')
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }

        # Step 2: Test & verify.
        response = self.authorized_client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_put(self):
        # Step 1: Delete any previous data.
        postal_addesses = ContactPoint.objects.all()
        for postal_address in postal_addesses.all():
            postal_addesses.delete()

        # Step 2: Set the location variables.
        url = reverse('contactpoint-list')+'1/'
        ContactPoint.objects.create(
            id=1,
            name="Unit Test",
            description="Used for unit testing purposes."
        )
        data = {
            'id': 1,
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }

        # Step 3: Test & verify.
        response = self.unauthorized_client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_put_with_authorization(self):
        # Step 1: Delete any previous data.
        postal_addesses = ContactPoint.objects.all()
        for postal_address in postal_addesses.all():
            postal_addesses.delete()

        # Step 2: Set the location variables.
        url = reverse('contactpoint-list')+'1/'
        ContactPoint.objects.create(
            id=1,
            name="Unit Test",
            description="Used for unit testing purposes.",
            owner_id=self.user.id
        )
        data = {
            'id': 1,
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }

        # Step 3: Test & verify.
        response = self.authorized_client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_delete(self):
        # Step 1: Set the location variables.
        url = reverse('contactpoint-list')+'1/'

        # Step 2: Test & verify.
        response = self.unauthorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_with_authentication(self):
        # Step 1: Set the location variables.
        url = reverse('contactpoint-list')+'1/'

        # Step 2: Test & verify.
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
