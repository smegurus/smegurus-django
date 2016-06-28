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
from base.models import BannedIP
from api.views import authentication
from api.models.privatefileupload import PrivateFileUpload

from django.core.urlresolvers import resolve, reverse
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient

TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIPrivateFileUploadTestCase(APITestCase, TenantTestCase):
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
        super(APIPrivateFileUploadTestCase, self).setUp()

        # Initialize our test data.
        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)

        # Setup.
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)

        PrivateFileUpload.objects.bulk_create([
            PrivateFileUpload(owner=self.user),
            PrivateFileUpload(owner=self.user),
            PrivateFileUpload(owner=self.user),
        ])

        # Above taken from:
        # http://www.django-rest-framework.org/api-guide/testing/#authenticating

    @transaction.atomic
    def tearDown(self):
        privatefileuploads = PrivateFileUpload.objects.all()
        for privatefileupload in privatefileuploads.all():
            privatefileupload.delete()

        users = User.objects.all()
        for user in users.all():
            user.delete()

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
        privatefileupload = PrivateFileUpload.objects.create(
            id=2030,
            owner=self.user,
        )
        privatefileupload.save()
        self.assertEqual(str(privatefileupload), "")

    @transaction.atomic
    def test_post_with_authenticated_user(self):
        # Step 1: Set the location variables.
        url = reverse('privatefileupload-list')
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
        url = reverse('privatefileupload-list')
        data = self._create_test_file('/tmp/test_upload')

        # Step 2: Perform a "multiform" post using AJAX.
        response = self.unauthorized_client.post(url, data, format='multipart')

        # Step 3: Test & verify.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list(self):
        # Step 1: Set the location variables.
        url = reverse('privatefileupload-list')

        # Step 2: Test & verify.
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_list_with_authentication(self):
        # Step 1: Set the location variables.
        url = reverse('privatefileupload-list')

        # Step 2: Test & verify.
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_list_with_banning(self):
        # Step 1: Setup variables.
        url = reverse('privatefileupload-list')

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
        uploads = PrivateFileUpload.objects.all()
        for upload in uploads.all():
            upload.delete()

        # Create a new object with our specific test data.
        PrivateFileUpload.objects.create(id=1,)

        # Run the test.
        url = reverse('privatefileupload-list')+'1/'
        response = self.unauthorized_client.put(url, json.dumps({'id': 1,}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_put_with_authorization(self):
        # Delete any previous data.
        uploads = PrivateFileUpload.objects.all()
        for upload in uploads.all():
            upload.delete()

        # Create a new object with our specific test data.
        PrivateFileUpload.objects.create(id=1, owner_id=self.user.id,)
        data = {
            'id': 1,
            'owner': self.user.id
        }

        # Run the test.
        url = reverse('privatefileupload-list')+'1/'
        response = self.authorized_client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_delete(self):
        # Step 1: Set the location variables.
        url = reverse('privatefileupload-list')+'1/'

        # Step 2: Test & verify.
        response = self.unauthorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_with_authentication(self):
        # Step 1: Set the location variables.
        url = reverse('privatefileupload-list')+'1/'

        # Step 2: Test & verify.
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
