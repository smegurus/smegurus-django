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


class RegistrationPublicViewsTestCases(APITestCase, TenantTestCase):
    fixtures = [
        'banned_domains.json',
        'banned_ips.json',
        'banned_words.json',
        'groups',
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
        super(RegistrationPublicViewsTestCases, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()

    @transaction.atomic
    def test_public_registration_page_view(self):
        response = self.c.get(reverse('public_registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        # self.assertIn(b'This is a land page.',response.content) #TODO: Change text

    @transaction.atomic
    def test_public_activation_required_page_view(self):
        response = self.c.get(reverse('public_activation_required'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        # self.assertIn(b'This is a land page.',response.content) #TODO: Change text

    @transaction.atomic
    def test_public_activate_page_view_with_success(self):
        """
        Unit test will take a User account which hasen't been activated and
        run the URL where activation happens and verify the User has been
        activated.
        """
        # Convert our User's ID into an encrypted value.
        user = User.objects.get(email=TEST_USER_EMAIL)
        user.is_activet = False
        user.save()
        signer = Signer()
        id_sting = str(user.id).encode()
        value = signer.sign(id_sting)

        # Run test.
        url = reverse('public_activation', args=[value])
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

        # Verify.
        user = User.objects.get(email=TEST_USER_EMAIL)
        self.assertTrue(user.is_active)

    @transaction.atomic
    def test_public_activate_page_view_with_failure(self):
        # Run test & verify.
        response = self.c.get(reverse('public_activation', args=['bad-value'] ))
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(response.content) > 1)
