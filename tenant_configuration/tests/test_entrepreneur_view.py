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
from foundation_public.models.organization import PublicOrganization
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.businessidea import BusinessIdea
from foundation_tenant.models.tag import Tag
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class FoundationConfigurationEntrepreneurViewsWithTenatSchemaTestCases(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galacticalliance'
        tenant.name = "Galactic Alliance of Humankind"
        tenant.has_perks=True
        tenant.has_mentors=True
        tenant.how_discovered = "Command HQ"
        tenant.how_many_served = 1

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
        super(FoundationConfigurationEntrepreneurViewsWithTenatSchemaTestCases, self).setUp()

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
        BusinessIdea.objects.delete_all()
        Tag.objects.delete_all()
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        TenantMe.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        groups = Group.objects.all()
        for group in groups.all():
            group.delete()
        # super(FoundationConfigurationEntrepreneurViewsWithTenatSchemaTestCases, self).tearDown()

    @transaction.atomic
    def test_config_entr_step_one_page_view_with_success(self):
        # Setup our User.
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(entrepreneur_group)
        self.user.save()

        # Test & verify.
        url = reverse('foundation_auth_config_entr_step_one')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_config_entr_step_one_page_view_with_failure(self):
        url = reverse('foundation_auth_config_entr_step_one')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def test_config_entr_step_two_page_view_with_success(self):
        # Setup our User.
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(entrepreneur_group)
        self.user.save()

        # Test & verify.
        url = reverse('foundation_auth_config_entr_step_two')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_config_entr_step_two_page_view_with_failure(self):
        url = reverse('foundation_auth_config_entr_step_two')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def test_config_entr_step_three_page_view_with_success(self):
        # Setup our User.
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(entrepreneur_group)
        self.user.save()

        # Test & verify.
        url = reverse('foundation_auth_config_entr_step_three')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_config_entr_step_three_page_view_with_failure(self):
        url = reverse('foundation_auth_config_entr_step_three')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def test_config_entr_step_four_page_view_with_success(self):
        # Setup our User.
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(entrepreneur_group)
        self.user.save()

        # Test & verify.
        url = reverse('foundation_auth_config_entr_step_four')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_config_entr_step_four_page_view_with_failure(self):
        url = reverse('foundation_auth_config_entr_step_four')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def test_config_entr_step_five_page_view_with_success(self):
        # Setup our User.
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(entrepreneur_group)
        self.user.save()

        # Test & verify.
        url = reverse('foundation_auth_config_entr_step_five')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_config_entr_step_five_page_view_with_failure(self):
        url = reverse('foundation_auth_config_entr_step_five')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
