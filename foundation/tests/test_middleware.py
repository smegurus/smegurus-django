import json
from django.db import transaction
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import User
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from rest_framework import status
from foundation.models import BannedIP


class BanEnforcingMiddlewareTestCase(TenantTestCase):
    """
    Unit Tests are used to make sure the HTML & JS get/post commands are
    properly handled by the Ban enforcing middleware.
    """
    fixtures = [
        'banned_domains.json',
        'banned_ips.json',
        'banned_words.json',
        # 'groups',
        # 'permissions',
    ]
    
    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English.
        super(BanEnforcingMiddlewareTestCase, self).setUp()
        self.client = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()

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
