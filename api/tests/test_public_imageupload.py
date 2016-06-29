import os
import json
from django.db import transaction
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from api.views import authentication
from foundation_public.models.banned import BannedIP
from foundation_public.models.imageupload import PublicImageUpload


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIPublicImageUploadTestCase(APITestCase, TenantTestCase):
    fixtures = [
        'banned_domains.json',
        'banned_ips.json',
        'banned_words.json',
        # 'groups',
        # 'permissions',
    ]

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
        super(APIPublicImageUploadTestCase, self).setUp()

        # Initialize our test data.
        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)

        # Setup.
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)

        # Above taken from:
        # http://www.django-rest-framework.org/api-guide/testing/#authenticating

        # Initialize our test data.
        PublicImageUpload.objects.bulk_create([
            PublicImageUpload(owner=self.user),
            PublicImageUpload(owner=self.user),
            PublicImageUpload(owner=self.user),
        ])

    @transaction.atomic
    def tearDown(self):
        """Delete all the images we uploaded for this Test"""
        image_uploads = PublicImageUpload.objects.all()
        for an_image in image_uploads.all():
            an_image.delete()

        users = User.objects.all()
        for user in users.all():
            user.delete()

    def _create_test_image(self, path):
        # Create the image.
        from PIL import Image
        width = 2
        height = 2
        img = Image.new('RGB', (width, height))
        img.save(path)

        # Open image.
        f = open(path, 'rb')
        return {'imagefile': f}

    @transaction.atomic
    def test_to_string(self):
        # Create a new object with our specific test data.
        upload = PublicImageUpload.objects.create(
            id=2030,
            owner=self.user,
        )
        upload.save()
        self.assertEqual(str(upload), "")

    @transaction.atomic
    def test_post_with_authenticated_user(self):
        # Step 1: Set the location variables.
        url = reverse('publicimageupload-list')
        data = self._create_test_image('/tmp/test_upload.png')
        data['owner'] = self.user.id

        # Step 2: Perform a "multiform" post using AJAX.
        response = self.authorized_client.post(url, data, format='multipart')

        # Step 3: Test & verify.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('created', response.data)

    @transaction.atomic
    def test_post(self):
        # Step 1: Set the location variables.
        url = reverse('publicimageupload-list')
        data = self._create_test_image('/tmp/test_upload.png')

        # Step 2: Perform a "multiform" post using AJAX.
        response = self.unauthorized_client.post(url, data, format='multipart')

        # Step 3: Test & verify.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_banning(self):
        # Step 1: Setup variables.
        url = reverse('publicimageupload-list')

        # Step 2: Ban self.
        BannedIP.objects.create(
            address='127.0.0.1',
            reason='For unit testing purposes.'
        )

        # Step 3: Test & verify.
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def test_list_with_authenticated_user(self):
        # Step 1: Setup variables.
        url = reverse('publicimageupload-list')

        # Step 2: Test & verify.
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    @transaction.atomic
    def test_list(self):
        # Step 1: Setup variables.
        url = reverse('publicimageupload-list')

        # Step 2: Test & verify.
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    @transaction.atomic
    def test_get_with_authenticated_user(self):
        # Step 1: Setup variables.
        url = reverse('publicimageupload-list')

        # Step 2: Test & verify.
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data) > 0, True)

    @transaction.atomic
    def test_get(self):
        # Step 1: Setup variables.
        url = reverse('publicimageupload-list')

        # Step 2: Test & verify.
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data) > 0, True)

    @transaction.atomic
    def test_put_with_authenticated_user(self):
        # Delete any previous data.
        uploads = PublicImageUpload.objects.all()
        for upload in uploads.all():
            upload.delete()

        # Create a new object with our specific test data.
        PublicImageUpload.objects.create(id=1, owner_id=self.user.id,)

        # Run the test.
        url = reverse('publicimageupload-list')+'1/'
        response = self.authorized_client.put(url, json.dumps({'id': 1, 'owner': self.user.id}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_put_with_different_owner(self):
        # Initialize our test user.
        user = User.objects.create_user(  # Create our user.
            email='h@h.com',
            username='h@h.com',
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()
        token = Token.objects.get(user=user)

        # Perform this unit test.
        # Step 1: Log in and get the first PublicImageUpload object.
        client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)

        # Delete any previous data.
        uploads = PublicImageUpload.objects.all()
        for upload in uploads.all():
            upload.delete()

        # Create a new object with our specific test data.
        PublicImageUpload.objects.create(id=1, owner_id=self.user.id,)

        # Run the test.
        url = reverse('publicimageupload-list')+'1/'
        response = client.put(url, json.dumps({'id': 1, 'owner': user.id }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def test_put(self):
        # Step 1: Set the location variables.
        url = reverse('publicimageupload-list')
        data = self._create_test_image('/tmp/test_upload.png')
        kwargs = {'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'}

        # Step 2: Perform a "multiform" post using AJAX.
        response = self.unauthorized_client.put(url,{
            'id': 1,
            'imagefile': data,
        }, **kwargs)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_with_authenticated_user(self):
        # Step 1: Delete any previous data.
        uploads = PublicImageUpload.objects.all()
        for upload in uploads.all():
            upload.delete()

        # Step 2: Setup variables.
        PublicImageUpload.objects.create(id=1, owner_id=self.user.id,)
        url = reverse('publicimageupload-list')+'1/'

        # Step 3: Test & verify.
        response = self.authorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def test_delete_with_different_owner(self):
        # Step 1: Delete any previous data.
        uploads = PublicImageUpload.objects.all()
        for upload in uploads.all():
            upload.delete()

        # Step 2: Initialize our test user.
        PublicImageUpload.objects.create(id=1, owner_id=self.user.id,)
        user = User.objects.create_user(  # Create our user.
            email='h@h.com',
            username='h@h.com',
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()
        token = Token.objects.get(user=user)

        # Step 3: Connect to the server.
        client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)

        # Step 4: Test & verify.
        url = reverse('publicimageupload-list')+'1/'
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def test_delete(self):
        # Step 1: Setup variables.
        url = reverse('publicimageupload-list')+'1/'

        # Step 2: Test & verify.
        response = self.unauthorized_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(response.data) > 0, True)
