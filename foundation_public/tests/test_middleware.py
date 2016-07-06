from django.db import transaction
from django.contrib.auth.models import User
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient


class CustomPublicMiddlewareTestCase(TenantTestCase):
    fixtures = [
        'banned_domains.json',
        'banned_ips.json',
        'banned_words.json',
        'groups',
        # 'permissions',
    ]

    @transaction.atomic
    def setUp(self):
        super(CustomPublicMiddlewareTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(CustomPublicMiddlewareTestCase, self).tearDown()

    @transaction.atomic
    def test_pass(self):
        pass

    #TODO: INVESTIGATE UTILIZING THESE UNIT TESTS.

    # @transaction.atomic
    # def test_list_with_banning(self):
    #     # Step 1: Setup variables.
    #     url = reverse('publicfileupload-list')
    #
    #     # Step 2: Ban self.
    #     BannedIP.objects.create(
    #         address='127.0.0.1',
    #         reason='For unit testing purposes.'
    #     )
    #
    #     # Step 3: Test & verify.
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    # @transaction.atomic
    # def test_list_without_banning(self):
    #     # Step 1: Setup variables.
    #     url = reverse('publicfileupload-list')
    #
    #     # Step 2: Ban self.
    #     BannedIP.objects.create(
    #         address='192.168.0.1',
    #         reason='For unit testing purposes.'
    #     )
    #
    #     # Step 3: Test & verify.
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
