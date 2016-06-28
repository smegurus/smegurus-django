import json
from django.db import transaction
from django.utils import translation
from rest_framework import status
from base.models import BannedIP

from django.core.urlresolvers import resolve, reverse
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient


class BanEnforcingMiddlewareTestCase(TenantTestCase):
    """
    Unit Tests are used to make sure the HTML & JS get/post commands are
    properly handled by the Ban enforcing middleware.
    """
    fixtures = []

    @classmethod
    def setUpTestData(cls):
        pass

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English.
        super(BanEnforcingMiddlewareTestCase, self).setUp()
        self.client = TenantClient(self.tenant)

    @transaction.atomic
    def test_access_denied(self):
        # Step 1: Ban ourself.
        BannedIP.objects.create(
            address='127.0.0.1',
            reason='For unit testing purposes.'
        )

        # Step 2: Test & verify.
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def test_access_granted(self):
        # Step 1: Ban ourself.
        BannedIP.objects.create(
            address='192.168.0.1',
            reason='For unit testing purposes.'
        )

        # Step 2: Test & verify.
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class APIBanEnforcingMiddlewareTestCase(APITestCase, TenantTestCase):
    """
    Unit Tests are used to make sure the API JSON get/post commands are properly
    handled by the Ban enforcing middleware.
    """
    fixtures = []

    @classmethod
    def setUpTestData(cls):
        pass

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English.
        super(APIBanEnforcingMiddlewareTestCase, self).setUp()
        self.client = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        pass

    @transaction.atomic
    def test_list_with_banning(self):
        # Step 1: Setup variables.
        url = reverse('publicfileupload-list')

        # Step 2: Ban self.
        BannedIP.objects.create(
            address='127.0.0.1',
            reason='For unit testing purposes.'
        )

        # Step 3: Test & verify.
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def test_list_without_banning(self):
        # Step 1: Setup variables.
        url = reverse('publicfileupload-list')

        # Step 2: Ban self.
        BannedIP.objects.create(
            address='192.168.0.1',
            reason='For unit testing purposes.'
        )

        # Step 3: Test & verify.
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
