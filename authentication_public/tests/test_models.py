from django.core import mail
from django.core.signing import Signer
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


class AuthenticationPublicModelsTestCases(APITestCase, TenantTestCase):
    fixtures = []

    @classmethod
    def setUpTestData(cls):
        pass

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English
        super(AuthenticationPublicModelsTestCases, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()

    @transaction.atomic
    def test_user_sends_activation_when_created_with_success(self):
        user = User.objects.create_user(  # Create our User.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Account Activation')
