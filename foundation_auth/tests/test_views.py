from django.core.signing import Signer
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_public.models.organization import PublicOrganization, PublicDomain
from foundation_public import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class FoundationAuthViewsWithPublicSchemaTestCases(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Public Schema"""
        tenant.schema_name = 'test'  # Do not change.
        tenant.name = "Galactic Alliance of Humankind"

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
        super(FoundationAuthViewsWithPublicSchemaTestCases, self).setUp()

        # Initialize our test data.
        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)

        # Setup.
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)
        self.authorized_client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

    @transaction.atomic
    def tearDown(self):
        super(FoundationAuthViewsWithPublicSchemaTestCases, self).tearDown()

    @transaction.atomic
    def test_user_registration_page_view(self):
        url = reverse('foundation_auth_user_registration')
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'ajax_new_user',response.content)

    @transaction.atomic
    def test_user_activation_required_page_view(self):
        response = self.unauthorized_client.get(reverse('foundation_auth_user_activation_required'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)

    @transaction.atomic
    def test_user_activate_page_view_with_success_for_entreprenuer(self):
        """
        Unit test will take a User account which hasen't been activated and
        run the URL where activation happens and verify the User has been
        activated.
        """
        # Convert our User's ID into an encrypted value.
        user = User.objects.get(email=TEST_USER_EMAIL)
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        user.is_activet = False
        user.groups.add(entrepreneur_group)
        user.save()
        signer = Signer()
        id_sting = str(user.id).encode()
        value = signer.sign(id_sting)
        self.tenant.users.add(user)
        self.tenant.save()

        # Run test.
        url = reverse('foundation_auth_user_activation', args=[value])
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)

        # Verify.
        user = User.objects.get(email=TEST_USER_EMAIL)
        self.assertTrue(user.is_active)

    @transaction.atomic
    def test_user_activate_page_view_with_success_for_org_admin(self):
        """
        Unit test will take a User account which hasen't been activated and
        run the URL where activation happens and verify the User has been
        activated.
        """
        # Convert our User's ID into an encrypted value.
        user = User.objects.get(email=TEST_USER_EMAIL)
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        user.is_activet = False
        user.groups.add(org_admin_group)
        user.save()
        signer = Signer()
        id_sting = str(user.id).encode()
        value = signer.sign(id_sting)
        self.tenant.users.add(user)
        self.tenant.save()

        # Run test.
        url = reverse('foundation_auth_user_activation', args=[value])
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)

        # Verify.
        user = User.objects.get(email=TEST_USER_EMAIL)
        self.assertTrue(user.is_active)

    @transaction.atomic
    def test_user_activate_page_view_with_failed_signiture(self):
        # Run test & verify.
        response = self.unauthorized_client.get(reverse('foundation_auth_user_activation', args=[666] ))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Failed activating this account.', response.content)

    @transaction.atomic
    def test_user_activate_page_view_with_missing_user(self):
        signer = Signer()
        id_sting = str(666).encode()
        value = signer.sign(id_sting)

        # Run test & verify.
        url = reverse('foundation_auth_user_activation', args=[value])
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(len(response.content) > 1)

    @transaction.atomic
    def test_user_login_page_view(self):
        response = self.unauthorized_client.get(reverse('foundation_auth_user_login'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)

    @transaction.atomic
    def test_org_reg_page_view(self):
        response = self.authorized_client.get(reverse('foundation_auth_org_registration'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)

    @transaction.atomic
    def test_org_successful_registration_view(self):
        # Assign User to Organization.
        self.tenant.users.add(self.user)
        self.tenant.owner = self.user
        self.tenant.save()

        # Run the test and verify.
        response = self.authorized_client.get(reverse('foundation_auth_org_successful_registration'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Successful Registration',response.content)

    @transaction.atomic
    def test_user_launchpad_page_view_with_unauthorized(self):
        response = self.unauthorized_client.get(reverse('foundation_auth_user_launchpad'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, '/en/login?next=/en/launchpad')

    @transaction.atomic
    def test_user_launchpad_page_view_with_redirect_to_org_reg(self):
        response = self.authorized_client.get(reverse('foundation_auth_user_launchpad'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, '/en/register/organization')

    @transaction.atomic
    def test_user_password_reset_page_view(self):
        url = reverse('foundation_auth_password_reset')
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'ajax_password_reset',response.content)


class FoundationAuthViewsWithTenatSchemaTestCases(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galacticalliance'
        tenant.name = "Galactic Alliance of Humankind"

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
        super(FoundationAuthViewsWithTenatSchemaTestCases, self).setUp()

        # Initialize our test data.
        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)

        # Setup.
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)
        self.authorized_client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Update Organization.
        self.tenant.users.add(self.user)
        self.tenant.save()

    @transaction.atomic
    def tearDown(self):
        super(FoundationAuthViewsWithTenatSchemaTestCases, self).tearDown()

    @transaction.atomic
    def test_user_launchpad_page_view_with_redirect_to_dashboard(self):
        url = reverse('foundation_auth_user_launchpad')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, 'http://galacticalliance.example.com/en/dashboard')
