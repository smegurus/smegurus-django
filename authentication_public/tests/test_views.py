from django.core.signing import Signer
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework.test import APITestCase
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_public import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class AuthenticationPublicViewsTestCases(APITestCase, TenantTestCase):
    fixtures = []

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(  # Create our User.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()

        Group.objects.bulk_create([
            Group(id=constants.ENTREPRENEUR_GROUP_ID, name="Entreprenuer",),
            Group(id=constants.MENTOR_GROUP_ID, name="Mentor",),
            Group(id=constants.ADVISOR_GROUP_ID, name="Advisor",),
            Group(id=constants.ORGANIZATION_MANAGER_GROUP_ID, name="Org Manager",),
            Group(id=constants.ORGANIZATION_ADMIN_GROUP_ID, name="Org Admin",),
            Group(id=constants.CLIENT_MANAGER_GROUP_ID, name="Client Manager",),
            Group(id=constants.SYSTEM_ADMIN_GROUP_ID, name="System Admin",),
        ])

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English
        super(AuthenticationPublicViewsTestCases, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()

        groups = Group.objects.all()
        for group in groups.all():
            group.delete()

    @transaction.atomic
    def test_public_user_authentication_page_view(self):
        response = self.c.get(reverse('public_user_registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        # self.assertIn(b'This is a land page.',response.content) #TODO: Change text

    @transaction.atomic
    def test_public_user_activation_required_page_view(self):
        response = self.c.get(reverse('public_user_activation_required'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        # self.assertIn(b'This is a land page.',response.content) #TODO: Change text

    @transaction.atomic
    def test_public_user_activate_page_view_with_success(self):
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
        url = reverse('public_user_activation', args=[value])
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

        # Verify.
        user = User.objects.get(email=TEST_USER_EMAIL)
        self.assertTrue(user.is_active)

    @transaction.atomic
    def test_public_user_activate_page_view_with_failure(self):
        # Run test & verify.
        response = self.c.get(reverse('public_user_activation', args=['bad-value'] ))
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(response.content) > 1)

    @transaction.atomic
    def test_public_user_login_page_view(self):
        response = self.c.get(reverse('public_user_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        # self.assertIn(b'This is a land page.',response.content) #TODO: Change text

    @transaction.atomic
    def test_public_user_launchpad_page_view_with_unauthorized(self):
        pass #TODO: Implement.

    @transaction.atomic
    def test_public_user_launchpad_page_view_with_redirect_to_org_reg(self):
        pass #TODO: Implement.

    @transaction.atomic
    def test_public_user_launchpad_page_view_with_redirect_to_dashboard(self):
        pass #TODO: Implement.

    @transaction.atomic
    def test_public_user_login_page_view(self):
        response = self.c.get(reverse('public_org_registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
