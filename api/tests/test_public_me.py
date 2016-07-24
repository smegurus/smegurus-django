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
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_public.models.me import PublicMe
from foundation_public import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRSTNAME = "Ledo"
TEST_USER_LASTNAME = ""


class APIPublicMeWithPublicSchemaTestCase(APITestCase, TenantTestCase):
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
            password=TEST_USER_PASSWORD,
            first_name=TEST_USER_FIRSTNAME,
            last_name=TEST_USER_LASTNAME,
        )
        user.is_active = True
        user.save()

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English
        super(APIPublicMeWithPublicSchemaTestCase, self).setUp()

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
        super(APIPublicMeWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_list_with_anonymous_user(self):
        response = self.unauthorized_client.get(reverse('publicme-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_owner(self):
        response = self.authorized_client.get(reverse('publicme-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_post_with_anonymous_user(self):
        data = {
            'owner': self.user.id
        }
        response = self.unauthorized_client.post(reverse('publicme-list'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_post_with_different_owner(self):
        # Change to a different user.
        user = User.objects.create(
            first_name='Hideauze',
            last_name='whalesquid',
            email='whalesquid@hideauze.com',
            password='123password'
        )
        user.is_active = True
        user.save()
        token = Token.objects.get(user=user)
        client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        data = {
            'owner': self.user.id
        }
        response = client.post(reverse('publicme-list'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_post_with_owner(self):
        data = {
            'owner': self.user.id
        }
        response = self.authorized_client.post(reverse('publicme-list'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_put_with_anonymous_user(self):
        # Delete any previous data.
        items = PublicMe.objects.all()
        for item in items.all():
            item.delete()

        # Create a new object with our specific test data.
        PublicMe.objects.create(
            id=1,
            owner=self.user
        )

        # Run the test.
        data = {
            'id': 1,
            'owner': self.user.id
        }
        response = self.unauthorized_client.put(reverse('publicme-list')+'1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_put_with_owner(self):
        # Delete any previous data.
        items = PublicMe.objects.all()
        for item in items.all():
            item.delete()

        # Create a new object with our specific test data.
        PublicMe.objects.create(
            id=1,
            owner=self.user
        )

        # Run the test.
        data = {
            'id': 1,
            'owner': self.user.id
        }
        response = self.authorized_client.put(reverse('publicme-list')+'1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_delete_with_anonymous_user(self):
        response = self.unauthorized_client.delete(reverse('publicme-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_with_owner(self):
        # Delete any previous data.
        items = PublicMe.objects.all()
        for item in items.all():
            item.delete()

        # Create our object to delete.
        item = PublicMe.objects.create(
            id=2030,
            owner=self.user
        )
        item.save()

        # Run our test and verify.
        response = self.authorized_client.delete(reverse('publicme-list')+'2030/',)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def test_unlock_with_success(self):
        # Delete any previous data.
        items = PublicMe.objects.all()
        for item in items.all():
            item.delete()

        # Create a new object with our specific test data.
        PublicMe.objects.create(
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
        response = self.authorized_client.put(reverse('publicme-list')+'1/unlock_me/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_unlock_with_missing_password(self):
        # Delete any previous data.
        items = PublicMe.objects.all()
        for item in items.all():
            item.delete()

        # Create a new object with our specific test data.
        PublicMe.objects.create(
            id=1,
            owner=self.user,
        )

        # Run the test.
        data = {
            'id': 1,
            'owner': self.user.id,
        }
        response = self.authorized_client.put(reverse('publicme-list')+'1/unlock_me/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def test_unlock_with_wrong_password(self):
        # Delete any previous data.
        items = PublicMe.objects.all()
        for item in items.all():
            item.delete()

        # Create a new object with our specific test data.
        PublicMe.objects.create(
            id=1,
            owner=self.user,
        )

        # Run the test.
        data = {
            'id': 1,
            'owner': self.user.id,
            'password': 'ILoveHideauze',
        }
        response = self.authorized_client.put(reverse('publicme-list')+'1/unlock_me/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
