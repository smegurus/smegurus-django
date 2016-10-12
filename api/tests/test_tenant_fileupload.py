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
from api.views import authentication
from foundation_public.models.banned import BannedIP
from foundation_tenant.models.fileupload import TenantFileUpload
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APITenantFileUploadWithTenantSchemaTestCase(APITestCase, TenantTestCase):
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
        super(APITenantFileUploadWithTenantSchemaTestCase, self).setUp()

        # Initialize our test data.
        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)

        # Setup.
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)

        TenantFileUpload.objects.bulk_create([
            TenantFileUpload(owner=self.user),
            TenantFileUpload(owner=self.user),
            TenantFileUpload(owner=self.user),
        ])

        # Above taken from:
        # http://www.django-rest-framework.org/api-guide/testing/#authenticating

    @transaction.atomic
    def tearDown(self):
        TenantFileUpload.objects.delete_all()
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        TenantMe.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(APITenantFileUploadWithTenantSchemaTestCase, self).tearDown()

    def _create_test_file(self, path):
        """
        Creates a simulated file.

        Source: https://medium.com/@jxstanford/django-rest-framework-file-upload-e4bc8de669c0#.l8dbmtosq
        """
        f = open(path, 'w')
        f.write('test123\n')
        f.close()
        f = open(path, 'rb')
        return {'datafile': f}

    @transaction.atomic
    def test_to_string(self):
        # Create a new object with our specific test data.
        entry = TenantFileUpload.objects.create(
            id=2030,
            owner=self.user,
        )
        entry.save()
        self.assertEqual(str(entry), "")

    @transaction.atomic
    def test_post_with_authenticated_user(self):
        # Step 1: Set the location variables.
        url = reverse('tenantfileupload-list')
        data = self._create_test_file('/tmp/test_upload')
        data['owner'] = self.user.id

        # Step 2: Perform a "multiform" post using AJAX.
        response = self.authorized_client.post(url, data, format='multipart')

        # Step 3: Test & verify.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('created', response.data)

    @transaction.atomic
    def test_post(self):
        # Step 1: Set the location variables.
        url = reverse('tenantfileupload-list')
        data = self._create_test_file('/tmp/test_upload')

        # Step 2: Perform a "multiform" post using AJAX.
        response = self.unauthorized_client.post(url, data, format='multipart')

        # Step 3: Test & verify.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list(self):
        # Step 1: Set the location variables.
        url = reverse('tenantfileupload-list')

        # Step 2: Test & verify.
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_list_with_authentication(self):
        # Step 1: Set the location variables.
        url = reverse('tenantfileupload-list')

        # Step 2: Test & verify.
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_list_with_banning(self):
        # Step 1: Setup variables.
        url = reverse('tenantfileupload-list')

        # Step 2: Ban self.
        BannedIP.objects.create(
            address='127.0.0.1',
            reason='For unit testing purposes.'
        )

        # Step 3: Test & verify.
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def test_put(self):
        # Delete any previous data.
        uploads = TenantFileUpload.objects.all()
        for upload in uploads.all():
            upload.delete()

        # Create a new object with our specific test data.
        TenantFileUpload.objects.create(id=1,)

        # Run the test.
        url = reverse('tenantfileupload-list')+'1/'
        response = self.unauthorized_client.put(url, json.dumps({'id': 1,}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_put_with_authorization(self):
        # Delete any previous data.
        uploads = TenantFileUpload.objects.all()
        for upload in uploads.all():
            upload.delete()

        # Create a new object with our specific test data.
        TenantFileUpload.objects.create(id=1, owner_id=self.user.id,)
        data = {
            'id': 1,
            'owner': self.user.id
        }

        # Run the test.
        url = reverse('tenantfileupload-list')+'1/'
        response = self.authorized_client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_delete(self):
        # Step 1: Set the location variables.
        url = reverse('tenantfileupload-list')+'1/'

        # Step 2: Test & verify.
        response = self.unauthorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_with_authentication(self):
        # Step 1: Delete any previous data.
        uploads = TenantFileUpload.objects.all()
        for upload in uploads.all():
            upload.delete()

        # Step 2: Set the location variables.
        TenantFileUpload.objects.create(id=1, owner_id=self.user.id,)
        url = reverse('tenantfileupload-list')+'1/'

        # Step 3: Test & verify.
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
