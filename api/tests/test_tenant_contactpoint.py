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
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.contactpoint import ContactPoint
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIContactPointWithTenantSchemaTestCase(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galacticalliance'
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
        super(APIContactPointWithTenantSchemaTestCase, self).setUp()

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
        ContactPoint.objects.delete_all()
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        Me.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(APIContactPointWithTenantSchemaTestCase, self).tearDown()

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
        response = self.unauthorized_client.get('/api/tenantcontactpoint/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_authentication(self):
        response = self.authorized_client.get('/api/tenantcontactpoint/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_post(self):
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }
        response = self.unauthorized_client.post('/api/tenantcontactpoint/', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_post_with_authentication(self):
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }
        response = self.authorized_client.post('/api/tenantcontactpoint/', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_put(self):
        # Delete any previous data.
        postal_addesses = ContactPoint.objects.all()
        for postal_address in postal_addesses.all():
            postal_addesses.delete()

        # Create a new object with our specific test data.
        ContactPoint.objects.create(
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
        response = self.unauthorized_client.put('/api/tenantcontactpoint/1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_put_with_authorization(self):
        # Delete any previous data.
        postal_addesses = ContactPoint.objects.all()
        for postal_address in postal_addesses.all():
            postal_addesses.delete()

        # Create a new object with our specific test data.
        ContactPoint.objects.create(
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
        response = self.authorized_client.put('/api/tenantcontactpoint/1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_delete(self):
        response = self.unauthorized_client.delete('/api/tenantcontactpoint/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_with_authentication(self):
        response = self.authorized_client.delete('/api/tenantcontactpoint/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
