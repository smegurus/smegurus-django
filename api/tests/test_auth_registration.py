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
from foundation_public.models.organization import PublicOrganization
from foundation_public import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIRegistrationWithPublicSchemaTestCase(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Public Schema"""
        tenant.schema_name = 'test'
        tenant.name = "Galactic Alliance of Humankind"

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
        super(APIRegistrationWithPublicSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        groups = Group.objects.all()
        for group in groups.all():
            group.delete()
        super(APIRegistrationWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_api_registration_with_success_for_org_admin(self):
        # Remove the existing user(s) before continuing.
        self.assertEqual(User.objects.count(), 1)
        for user in User.objects.all():
            user.delete()
        self.assertEqual(User.objects.count(), 0)

        # Perform the Unit-Tests
        url = reverse('api_register')
        data = {
            'username': 'whalesquid@hideauze.com',
            'email': 'whalesquid@hideauze.com',
            'password': 'test',
            'first_name': 'Transhumanist',
            'last_name': '#1'
        }
        response = self.c.post(url, data, format='json')

        # Verify general info.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'whalesquid@hideauze.com')
        group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)

        # Verify group membership.
        is_org_admin = False
        for a_group in User.objects.get().groups.all():
            if a_group == group:
                is_org_admin = True
        self.assertEqual(is_org_admin, True)

    @transaction.atomic
    def test_api_registration_with_failure(self):
        self.assertEqual(User.objects.count(), 1)
        url = reverse('api_register')
        data = {
            'username': TEST_USER_USERNAME,
            'email': TEST_USER_EMAIL,
            'password': TEST_USER_PASSWORD,
            'first_name': 'Ledo',
            'last_name': 'Clone #123'
        }
        response = self.c.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, TEST_USER_EMAIL)


class APIRegistrationWithTenantSchemaTestCase(APITestCase, TenantTestCase):

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galacticalliance'
        tenant.name = "Galactic Alliance of Humankind"

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
        super(APIRegistrationWithTenantSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        groups = Group.objects.all()
        for group in groups.all():
            group.delete()
        super(APIRegistrationWithTenantSchemaTestCase, self).tearDown()


    @transaction.atomic
    def test_api_registration_with_success_for_entrepreneur(self):
        # Remove the existing user(s) before continuing.
        self.assertEqual(User.objects.count(), 1)
        for user in User.objects.all():
            user.delete()
        self.assertEqual(User.objects.count(), 0)

        # Perform the Unit-Tests
        response = self.c.get(reverse('api_register'))
        url = reverse('api_register')
        data = {
            'username': 'whalesquid@hideauze.com',
            'email': 'whalesquid@hideauze.com',
            'password': 'test',
            'first_name': 'Transhumanist',
            'last_name': '#1'
        }
        response = self.c.post(url, data, format='json')

        # Verify general info.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'whalesquid@hideauze.com')
        group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)

        # Verify group membership.
        is_entrepreneur = False
        for a_group in User.objects.get().groups.all():
            if a_group == group:
                is_entrepreneur = True
        self.assertEqual(is_entrepreneur, True)
