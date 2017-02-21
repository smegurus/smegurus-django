from django.db import transaction
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django_tenants.test.cases import FastTenantTestCase
from django_tenants.test.client import TenantClient
from smegurus import constants
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.contactpoint import ContactPoint
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.slide import Slide


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRST_NAME = "Ledo"
TEST_USER_LAST_NAME = ""


class TenantWorkspaceModuleTestCases(APITestCase, FastTenantTestCase):
    fixtures = []

    @staticmethod
    def get_test_schema_name():
        return 'galacticalliance'

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galacticalliance'
        tenant.name = "Galactic Alliance of Humankind"
        tenant.is_setup = True
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
        # super(TenantRewardTestCases, self).setUp()

        # Initialize our test data.
        self.user = User.objects.get(username=TEST_USER_USERNAME)
        token = Token.objects.get(user=self.user)

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

        # Setup User.
        self.me = Me.objects.create(
            owner=self.user,
        )
        self.workspace = Workspace.objects.create(
            name="Test Workspace"
        )
        self.workspace.owners.add(self.user)
        self.module = Module.objects.create(
            workspace=self.workspace,
            title="Test Module"
        )

    @transaction.atomic
    def tearDown(self):
        Slide.objects.delete_all()
        Workspace.objects.delete_all()
        Module.objects.delete_all()
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        Me.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()

    @transaction.atomic
    def test_workspace_module_master_page(self):
        pass

        # url = reverse('tenant_workspace_master', args=[self.workspace.id,])
        # response = self.authorized_client.get(url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertTrue(len(response.content) > 1)
        # self.assertIn(b'Workspace',response.content)
