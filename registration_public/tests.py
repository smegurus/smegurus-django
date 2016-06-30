from django.db import transaction
from django.contrib.auth.models import User
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework.test import APITestCase
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class RegistrationPublicTestCases(APITestCase, TenantTestCase):
    fixtures = [
        'banned_domains.json',
        'banned_ips.json',
        'banned_words.json',
        # 'groups',
        # 'permissions',
    ]

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(  # Create our User.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English
        super(RegistrationPublicTestCases, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()

    @transaction.atomic
    def test_org_owner_registration_page_view(self):
        response = self.c.get(reverse('org_owner_registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        # self.assertIn(b'This is a land page.',response.content) #TODO: Change text

    @transaction.atomic
    def test_org_owner_activation_required_page_view(self):
        response = self.c.get(reverse('org_owner_activation_required'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        # self.assertIn(b'This is a land page.',response.content) #TODO: Change text
