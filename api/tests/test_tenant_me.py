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
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.intake import Intake
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRSTNAME = "Ledo"
TEST_USER_LASTNAME = ""


class APITenantMeWithTenantSchemaTestCase(APITestCase, TenantTestCase):
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
        super(APITenantMeWithTenantSchemaTestCase, self).setUp()

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

    @transaction.atomic
    def tearDown(self):
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        Intake.objects.delete_all()
        TenantMe.objects.delete_all()
        items = User.objects.all()
        for item in items.all():
            item.delete()
        # super(APITenantMeWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_list(self):
        response = self.unauthorized_client.get('/api/tenantme/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_authentication(self):
        response = self.authorized_client.get('/api/tenantme/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_post_with_anonymous_user(self):
        data = {
            'owner': self.user.id
        }
        response = self.unauthorized_client.post('/api/tenantme/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_post_with_authenticated_owner(self):
        data = {
            'owner': self.user.id,
        }
        response = self.authorized_client.post(
            '/api/tenantme/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_put(self):
        # Delete any previous data.
        items = TenantMe.objects.delete_all()

        # Create a new object with our specific test data.
        TenantMe.objects.create(
            id=1,
            owner=self.user,
        )

        # Run the test.
        data = {
            'id': 1,
            'owner': self.user.id
        }
        response = self.unauthorized_client.put('/api/tenantme/1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_put_with_authorization(self):
        # Create a new object with our specific test data.
        address = PostalAddress.objects.create(
            owner=self.user,
            name='User #' + str(self.user.id) + ' Address',
        )
        contact_point = ContactPoint.objects.create(
            owner=self.user,
            name='User #' + str(self.user.id) + ' Contact Point',
        )
        TenantMe.objects.create(
            id=1,
            owner_id=self.user.id,
            address=address,
            contact_point=contact_point,
        )

        # Run the test.
        data = {
            'id': 1,
            'owner': self.user.id,
            'address': address.id,
            'contact_point': contact_point.id
        }
        response = self.authorized_client.put('/api/tenantme/1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_delete(self):
        response = self.unauthorized_client.delete('/api/tenantme/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_with_authentication_case_one(self):
        address = PostalAddress.objects.create(
            id=1,
            owner=self.user,
        )
        contact_point = ContactPoint.objects.create(
            id=1,
            owner=self.user,
        )
        me = TenantMe.objects.create(
            id=666,
            owner=self.user,
        )
        Intake.objects.create(
            id=1,
            me=me,
        )
        response = self.authorized_client.delete('/api/tenantme/'+str(me.id)+'/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def test_delete_with_authentication_case_two(self):
        me = TenantMe.objects.create(
            id=666,
            owner=self.user,
        )
        response = self.authorized_client.delete('/api/tenantme/'+str(me.id)+'/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def test_delete_with_authentication_case_three(self):
        group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(group)
        me = TenantMe.objects.create(
            id=999,
            owner=self.user,
        )
        response = self.authorized_client.delete('/api/tenantme/'+str(me.id)+'/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_admit_me_with_entrepreneur_user(self):
        # Setup our object.
        TenantMe.objects.create(
            id=1,
            owner=self.user,
            is_admitted=False,
        )

        # Run the test and verify.
        response = self.authorized_client.put(
            '/api/tenantme/1/admit_me/',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        me = TenantMe.objects.get(id=1)
        self.assertFalse(me.is_admitted)

    @transaction.atomic
    def test_admit_me_with_org_manager_user(self):
        # Setup our object.
        TenantMe.objects.create(
            id=1,
            owner=self.user,
            is_admitted=False,
        )
        group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(group)
        self.user.save()

        # Run the test and verify.
        response = self.authorized_client.put(
            '/api/tenantme/1/admit_me/',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        me = TenantMe.objects.get(id=1)
        self.assertTrue(me.is_admitted)

    @transaction.atomic
    def test_expel_me_with_entrepreneur_user(self):
        # Setup our object.
        TenantMe.objects.create(
            id=1,
            owner=self.user,
            is_admitted=True,
        )

        # Run the test and verify.
        response = self.authorized_client.put(
            '/api/tenantme/1/expel_me/',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        me = TenantMe.objects.get(id=1)
        self.assertTrue(me.is_admitted)

    @transaction.atomic
    def test_expel_me_with_org_manager_user(self):
        # Setup our object.
        TenantMe.objects.create(
            id=1,
            owner=self.user,
            is_admitted=True,
        )
        group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(group)
        self.user.save()

        # Run the test and verify.
        response = self.authorized_client.put(
            '/api/tenantme/1/expel_me/',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        me = TenantMe.objects.get(id=1)
        self.assertFalse(me.is_admitted)

    @transaction.atomic
    def test_unlock_with_success(self):
        # Delete any previous data.
        items = TenantMe.objects.delete_all()

        # Create a new object with our specific test data.
        TenantMe.objects.create(
            id=1,
            owner=self.user,
            is_locked=False,
        )

        # Run the test.
        data = {
            'id': 1,
            'owner': self.user.id,
            'password': TEST_USER_PASSWORD
        }
        response = self.authorized_client.put(
            '/api/tenantme/1/unlock_me/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_unlock_with_missing_password(self):
        # Delete any previous data.
        items = TenantMe.objects.delete_all()

        # Create a new object with our specific test data.
        TenantMe.objects.create(
            id=1,
            owner=self.user,
        )

        # Run the test.
        data = {
            'id': 1,
            'owner': self.user.id,
        }
        response = self.authorized_client.put(
            '/api/tenantme/1/unlock_me/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_unlock_with_wrong_password(self):
        # Delete any previous data.
        items = TenantMe.objects.delete_all()

        # Create a new object with our specific test data.
        TenantMe.objects.create(
            id=1,
            owner=self.user,
        )

        # Run the test.
        data = {
            'id': 1,
            'owner': self.user.id,
            'password': 'ILoveHideauze',
        }
        response = self.authorized_client.put(
            '/api/tenantme/1/unlock_me/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
