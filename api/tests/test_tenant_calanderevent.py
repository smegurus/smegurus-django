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
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.calendarevent import CalendarEvent
from foundation_tenant.models.base.me import TenantMe
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.contactpoint import ContactPoint
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APICalendarEventWithTenantSchemaTestCase(APITestCase, TenantTestCase):
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
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        user = User.objects.create_user(  # Create our user.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_superuser = True
        user.is_active = True
        user.groups.add(org_admin_group)
        user.save()

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English.
        super(APICalendarEventWithTenantSchemaTestCase, self).setUp()

        # Initialize our test data.
        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)

        # Setup.
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)
        self.authorized_client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        self.tenant.owner = self.user
        self.tenant.save()

        # Above taken from:
        # http://www.django-rest-framework.org/api-guide/testing/#authenticating

        # Initialize our test data.
        Tag.objects.bulk_create([
            Tag(name='1'),
            Tag(name='2'),
            Tag(name='3'),
        ])

    @transaction.atomic
    def tearDown(self):
        CalendarEvent.objects.delete_all()
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        TenantMe.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(APICalendarEventWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_list_with_anonymous_user(self):
        response = self.unauthorized_client.get('/api/tenantcalendarevent/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_authenticated_management_group_user(self):
        response = self.authorized_client.get('/api/tenantcalendarevent/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_list_with_authenticated_advisor_group_user(self):
        # Change Group that the User belongs in.
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.remove(org_admin_group)
        self.user.groups.add(advisor_group)
        self.user.save()

        # Test and verify.
        response = self.authorized_client.get('/api/tenantcalendarevent/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_post_with_anonymous_user(self):
        data = {
            'name': 'Unit Test',
        }
        response = self.unauthorized_client.post('/api/tenantcalendarevent/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_post_with_authenticated_management_group_user(self):
        # Run the test and verify.
        data = {
            'name': 'Unit Test',
        }
        response = self.authorized_client.post('/api/tenantcalendarevent/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_post_with_authenticated_advisor_group_user(self):
        # Change Group that the User belongs in.
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.remove(org_admin_group)
        self.user.groups.add(advisor_group)
        self.user.save()

        # Test and verify.
        data = {
            'name': 'Unit Test',
        }
        response = self.authorized_client.post('/api/tenantcalendarevent/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_put_with_anonymous_user(self):
        # Create a new object with our specific test data.
        CalendarEvent.objects.create(
            id=1,
            name="Unit Test",
        )

        # Run the test.
        data = {
            'id': 1,
            'name': 'Unit Test',
        }
        response = self.unauthorized_client.put('/api/tenantcalendarevent/1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_put_with_authenticated_management_user(self):
        # Create a new object with our specific test data.
        CalendarEvent.objects.create(
            id=1,
            name="Unit Test",
        )

        # Run the test.
        data = {
            'id': 1,
            'name': 'Unit Test',
        }
        response = self.authorized_client.put('/api/tenantcalendarevent/1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_put_with_authenticated_advisor_user(self):
        # Change Group that the User belongs in.
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.remove(org_admin_group)
        self.user.groups.add(advisor_group)
        self.user.save()

        # Create a new object with our specific test data.
        CalendarEvent.objects.create(
            id=1,
            name="Unit Test",
        )

        # Run the test.
        data = {
            'id': 1,
            'name': 'Unit Test',
        }
        response = self.authorized_client.put('/api/tenantcalendarevent/1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_delete_with_anonymous_user(self):
        response = self.unauthorized_client.delete('/api/tenantcalendarevent/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_with_authenticated_management_user(self):
        # Create a new object with our specific test data.
        CalendarEvent.objects.create(
            id=1,
            name="Unit Test",
        )

        # Test and verify.
        response = self.authorized_client.delete('/api/tenantcalendarevent/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def test_delete_with_authenticated_advisor_user(self):
        # Change Group that the User belongs in.
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.remove(org_admin_group)
        self.user.groups.add(advisor_group)
        self.user.save()

        # Create a new object with our specific test data.
        CalendarEvent.objects.create(
            id=1,
            name="Unit Test",
        )

        # Run test and verify.
        response = self.authorized_client.delete('/api/tenantcalendarevent/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
