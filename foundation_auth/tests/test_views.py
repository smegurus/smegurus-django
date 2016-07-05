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
from foundation_public.models.organization import PublicOrganization, Domain
from foundation_public import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class FoundationAuthViewsTestCases(APITestCase, TenantTestCase):
    fixtures = []

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

    def setup_tenant(self, tenant):
        """
        Add any additional setting to the tenant before it get saved. This is required if you have
        required fields.
        """
        tenant.name = "SME Gurus"

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English
        super(FoundationAuthViewsTestCases, self).setUp()

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
        users = User.objects.all()
        for user in users.all():
            user.delete()

        groups = Group.objects.all()
        for group in groups.all():
            group.delete()

    @transaction.atomic
    def test_user_registration_page_view(self):
        url = reverse('foundation_auth_user_registration')
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        # self.assertIn(b'ajax_new_user',response.content)

    @transaction.atomic
    def test_user_activation_required_page_view(self):
        response = self.unauthorized_client.get(reverse('foundation_auth_user_activation_required'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

    @transaction.atomic
    def test_user_activate_page_view_with_success(self):
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
        self.tenant.users.add(user)
        self.tenant.save()

        # Run test.
        url = reverse('foundation_auth_user_activation', args=[value])
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

        # Verify.
        user = User.objects.get(email=TEST_USER_EMAIL)
        self.assertTrue(user.is_active)

    @transaction.atomic
    def test_user_activate_page_view_with_failure(self):
        # Run test & verify.
        response = self.unauthorized_client.get(reverse('foundation_auth_user_activation', args=['bad-value'] ))
        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(response.content) > 1)

    @transaction.atomic
    def test_user_login_page_view(self):
        response = self.unauthorized_client.get(reverse('foundation_auth_user_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        # self.assertIn(b'This is a land page.',response.content) #TODO: Change text

    @transaction.atomic
    def test_org_reg_page_view(self):
        response = self.authorized_client.get(reverse('foundation_auth_org_registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)

    @transaction.atomic
    def test_org_successful_registration_view(self):
        user = User.objects.get(email=TEST_USER_EMAIL)
        with PublicOrganization(schema_name='public'):
           # Create tenant in this block
            org = PublicOrganization.objects.create(schema_name="test_mikasoftware", owner=user,)

            # Test
            response = self.authorized_client.get(reverse('foundation_auth_org_successful_registration'))

            # Verify
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(response.content) > 1)
            self.assertIn(b'test_mikasoftware',response.content)
            
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

    # @transaction.atomic
    # def test_user_launchpad_page_view_with_redirect_to_dashboard(self):
    #     with PublicOrganization(schema_name='public', owner=self.user):
    #         new_tenant = PublicOrganization.objects.create(schema_name='mikasoftware', owner=self.user)
    #         domain = Domain()
    #         domain.domain = 'localhost' # don't add your port or www here! on a local server you'll want to use localhost here
    #         domain.tenant = new_tenant
    #         domain.is_primary = True
    #         try:
    #             domain.save()
    #         except Exception as e:
    #             print(e)
    #
    #         token = Token.objects.get(user__username=TEST_USER_USERNAME)
    #         self.authorized_client = TenantClient(new_tenant, HTTP_AUTHORIZATION='Token ' + token.key)
    #         self.authorized_client.login(
    #             username=TEST_USER_USERNAME,
    #             password=TEST_USER_PASSWORD
    #         )
    #
    #         url = reverse('foundation_auth_user_launchpad')
    #         # url = 'http://mikasoftware.localhost/en/launchpad'
    #         print(url)
    #         response = self.authorized_client.get(url)
    #         self.assertEqual(response.status_code, status.HTTP_302_FOUND) #TODO: Figure out 404 error?
    #         self.assertRedirects(response, 'http://mikasoftware.example.com/en/dashboard')
