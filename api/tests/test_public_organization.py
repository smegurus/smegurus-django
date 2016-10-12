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
from foundation_public.models.organization import PublicOrganization
from foundation_public.models.banned import BannedWord
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIPublicOrganizationWithPublicSchemaTestCase(APITestCase, TenantTestCase):
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
        translation.activate('en')  # Set English
        super(APIPublicOrganizationWithPublicSchemaTestCase, self).setUp()

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

    @transaction.atomic
    def tearDown(self):
        super(APIPublicOrganizationWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_list(self):
        response = self.unauthorized_client.get(reverse('publicorganization-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_authentication(self):
        response = self.authorized_client.get('/api/publicorganization/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_post(self):
        data = {
            'schema_name': 'galacticalliance',
            'name': 'Galactic Alliance of Humankind',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }
        response = self.unauthorized_client.post('/api/publicorganization/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_post_with_upper_case_schema_name(self):
        data = {
            'schema_name': 'GalacticAlliance',
            'name': 'Galactic Alliance of Humankind',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }
        response = self.authorized_client.post('/api/publicorganization/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_post_with_non_alpha_schema_name(self):
        data = {
            'schema_name': 'ak47',
            'name': 'Galactic Alliance of Humankind',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }
        response = self.authorized_client.post('/api/publicorganization/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_post_with_special_characters_in_schema_name(self):
        data = {
            'schema_name': 'chambers@galacticalliance.com',
            'name': 'Galactic Alliance of Humankind',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }
        response = self.authorized_client.post('/api/publicorganization/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_post_with_whitespace_in_schema_name(self):
        data = {
            'schema_name': 'galactic alliance',
            'name': 'Galactic Alliance of Humankind',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }
        response = self.authorized_client.post('/api/publicorganization/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_post_with_reserved_word_in_schema_name(self):
        data = {
            'schema_name': 'api',
            'name': 'Galactic Alliance of Humankind',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }
        response = self.authorized_client.post('/api/publicorganization/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_post_with_banned_word_in_schema_name(self):
        # Create our BannedWord
        BannedWord.objects.create(
            text='hideauze',
            reason='They are the enemoy of humankind',
        )

        # Run our test and verify.
        data = {
            'schema_name': 'hideauze',
            'name': 'Galactic Alliance of Humankind',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id
        }
        response = self.authorized_client.post('/api/publicorganization/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#TODO: Implement the rest.
    # @transaction.atomic
    # def test_post_with_authentication(self):
    #     data = {
    #         'schema_name': 'galacticalliance',
    #         'name': 'Galactic Alliance of Humankind',
    #         'description': 'Used for unit testing purposes.',
    #         'owner': self.user.id
    #     }
    #     response = self.authorized_client.post('/api/publicorganization/', json.dumps(data), content_type='application/json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# class APIPublicOrganizationWithTenantSchemaTestCase(APITestCase, TenantTestCase):
#     fixtures = []
#
#     def setup_tenant(self, tenant):
#         """Tenant Schema"""
#         tenant.schema_name = 'galacticalliance'
#         tenant.name = "Galactic Alliance of Humankind"
#
#     @classmethod
#     def setUpTestData(cls):
#         Group.objects.bulk_create([
#             Group(id=constants.ENTREPRENEUR_GROUP_ID, name="Entreprenuer",),
#             Group(id=constants.MENTOR_GROUP_ID, name="Mentor",),
#             Group(id=constants.ADVISOR_GROUP_ID, name="Advisor",),
#             Group(id=constants.ORGANIZATION_MANAGER_GROUP_ID, name="Org Manager",),
#             Group(id=constants.ORGANIZATION_ADMIN_GROUP_ID, name="Org Admin",),
#             Group(id=constants.CLIENT_MANAGER_GROUP_ID, name="Client Manager",),
#             Group(id=constants.SYSTEM_ADMIN_GROUP_ID, name="System Admin",),
#         ])
#
#         user = User.objects.create_user(  # Create our user.
#             email=TEST_USER_EMAIL,
#             username=TEST_USER_USERNAME,
#             password=TEST_USER_PASSWORD
#         )
#         user.is_active = True
#         user.save()
#
#     @transaction.atomic
#     def setUp(self):
#         translation.activate('en')  # Set English
#         super(APIPublicOrganizationWithTenantSchemaTestCase, self).setUp()
#         self.c = TenantClient(self.tenant)
#
#     @transaction.atomic
#     def tearDown(self):
#         super(APIPublicOrganizationWithTenantSchemaTestCase, self).tearDown()
#
#     @transaction.atomic
#     def test_api_pass(self):
#         pass
#
# #TODO: Implement the rest.
