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
from tenant_schemas.test.cases import TenantTestCase
from tenant_schemas.test.client import TenantClient
from foundation_tenant.models.communitypost import CommunityPost
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APICommunityPostWithTenantSchemaTestCase(APITestCase, TenantTestCase):
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
        user.is_superuser = True
        user.is_active = True
        user.save()

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English.
        super(APICommunityPostWithTenantSchemaTestCase, self).setUp()

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
        CommunityPost.objects.bulk_create([
            CommunityPost(name='1', owner=self.user,),
            CommunityPost(name='2', owner=self.user,),
            CommunityPost(name='3', owner=self.user,),
        ])

    @transaction.atomic
    def tearDown(self):
        CommunityPost.objects.delete_all()
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        TenantMe.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(APICommunityPostWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_list_with_anonymous_user(self):
        response = self.unauthorized_client.get('/api/tenantcommunitypost/?format=json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_authenticated_management_group_user(self):
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(org_admin_group)

        response = self.authorized_client.get('/api/tenantcommunitypost/?format=json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_list_with_authenticated_advisor_group_user(self):
        # Change Group that the User belongs in.
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.add(advisor_group)
        self.user.save()

        # Test and verify.
        response = self.authorized_client.get('/api/tenantcommunitypost/?format=json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_post_with_anonymous_user(self):
        data = {
            'name': 'Unit Test',
            'owner': self.user.id,
        }
        response = self.unauthorized_client.post(
            '/api/tenantcommunitypost/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_post_with_authenticated_management_group_user(self):
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(org_admin_group)
        self.user.save()

        # Run the test and verify.
        data = {
            'name': 'Unit Test',
            'owner': self.user.id,
        }
        response = self.authorized_client.post(
            '/api/tenantcommunitypost/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_post_with_authenticated_entrepreneur_group_user(self):
        group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(group)
        self.user.save()

        # Run the test and verify.
        data = {
            'name': 'Unit Test',
            'owner': self.user.id,
        }
        response = self.authorized_client.post(
            '/api/tenantcommunitypost/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_post_with_authenticated_advisor_group_user(self):
        # Change Group that the User belongs in.
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.add(advisor_group)
        self.user.save()

        # Test and verify.
        data = {
            'name': 'Unit Test',
            'owner': self.user.id,
        }
        response = self.authorized_client.post(
            '/api/tenantcommunitypost/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_put_with_anonymous_user(self):
        # Create a new object with our specific test data.
        CommunityPost.objects.create(
            id=666,
            name="Unit Test",
            owner=self.user,
        )

        # Run the test.
        data = {
            'id': 666,
            'name': 'Unit Test',
            'owner': self.user.id,
        }
        response = self.unauthorized_client.put(
            '/api/tenantcommunitypost/666/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_put_with_authenticated_management_user(self):
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(org_admin_group)
        self.user.save()

        # Create a new object with our specific test data.
        CommunityPost.objects.create(
            id=666,
            name="Unit Test",
            owner=self.user,
        )

        # Run the test.
        data = {
            'id': 666,
            'name': 'Unit Test',
            'owner': self.user.id,
        }
        response = self.authorized_client.put(
            '/api/tenantcommunitypost/666/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_put_with_authenticated_advisor_user(self):
        # Change Group that the User belongs in.
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.add(advisor_group)
        self.user.save()

        # Create a new object with our specific test data.
        CommunityPost.objects.create(
            id=666,
            name="Unit Test",
            owner=self.user,
        )

        # Run the test.
        data = {
            'id': 666,
            'name': 'Unit Test',
            'owner': self.user.id,
        }
        response = self.authorized_client.put(
            '/api/tenantcommunitypost/666/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_delete_with_anonymous_user(self):
        response = self.unauthorized_client.delete('/api/tenantcommunitypost/1/?format=json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_with_authenticated_management_user(self):
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(org_admin_group)
        self.user.save()
        response = self.authorized_client.delete('/api/tenantcommunitypost/1/?format=json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def test_delete_with_authenticated_advisor_user(self):
        # Change Group that the User belongs in.
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.add(advisor_group)
        self.user.save()

        # Run test and verify.
        response = self.authorized_client.delete('/api/tenantcommunitypost/1/?format=json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def test_like_with_anonymous_user(self):
        response = self.unauthorized_client.put(
            '/api/tenantcommunitypost/1/like/?format=json',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_like_with_authenticated_entrepreneur_user(self):
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(entrepreneur_group)
        self.user.save()

        response = self.authorized_client.put(
            '/api/tenantcommunitypost/1/like/?format=json',
            json.dumps({}), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_like_with_authenticated_management_user(self):
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(org_admin_group)
        self.user.save()

        response = self.authorized_client.put(
            '/api/tenantcommunitypost/1/like/?format=json',
            json.dumps({}), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_like_with_authenticated_advisor_user(self):
        # Change Group that the User belongs in.
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.add(advisor_group)
        self.user.save()

        response = self.authorized_client.put(
            '/api/tenantcommunitypost/1/like/?format=json',
            json.dumps({}), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_unlike_with_anonymous_user(self):
        response = self.unauthorized_client.put(
            '/api/tenantcommunitypost/1/unlike/?format=json',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_unlike_with_authenticated_entrepreneur_user(self):
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(entrepreneur_group)
        self.user.save()

        response = self.authorized_client.put(
            '/api/tenantcommunitypost/1/unlike/?format=json',
            json.dumps({}), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_unlike_with_authenticated_management_user(self):
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(org_admin_group)
        self.user.save()

        response = self.authorized_client.put(
            '/api/tenantcommunitypost/1/unlike/?format=json',
            json.dumps({}), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_unlike_with_authenticated_advisor_user(self):
        # Change Group that the User belongs in.
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.add(advisor_group)
        self.user.save()

        response = self.authorized_client.put(
            '/api/tenantcommunitypost/1/unlike/?format=json',
            json.dumps({}), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
