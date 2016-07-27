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
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.intake import Intake


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRSTNAME = "Ledo"
TEST_USER_LASTNAME = ""


# class TenantIntakeDecoratorWithPublicSchemaTestCase(APITestCase, TenantTestCase):
#     fixtures = []
#
#     def setup_tenant(self, tenant):
#         """Public Schema"""
#         tenant.schema_name = 'test'
#         tenant.name = "Galactic Alliance of Humankind"
#
#     @transaction.atomic
#     def setUp(self):
#         translation.activate('en')  # Set English
#         super(TenantIntakeDecoratorWithPublicSchemaTestCase, self).setUp()
#
#         # Initialize our test data.
#         Group.objects.bulk_create([
#             Group(id=constants.ENTREPRENEUR_GROUP_ID, name="Entreprenuer",),
#             Group(id=constants.MENTOR_GROUP_ID, name="Mentor",),
#             Group(id=constants.ADVISOR_GROUP_ID, name="Advisor",),
#             Group(id=constants.ORGANIZATION_MANAGER_GROUP_ID, name="Org Manager",),
#             Group(id=constants.ORGANIZATION_ADMIN_GROUP_ID, name="Org Admin",),
#             Group(id=constants.CLIENT_MANAGER_GROUP_ID, name="Client Manager",),
#             Group(id=constants.SYSTEM_ADMIN_GROUP_ID, name="System Admin",),
#         ])
#
#         self.user = User.objects.create_user(  # Create our User.
#             email=TEST_USER_EMAIL,
#             username=TEST_USER_USERNAME,
#             password=TEST_USER_PASSWORD
#         )
#         self.user.is_active = True
#         self.user.save()
#         token = Token.objects.get(user__username=TEST_USER_USERNAME)
#
#         # Setup.
#         self.unauthorized_client = TenantClient(self.tenant)
#         self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)
#         self.authorized_client.login(
#             username=TEST_USER_USERNAME,
#             password=TEST_USER_PASSWORD
#         )
#
#         # Update Organization.
#         self.tenant.users.add(self.user)
#         self.tenant.save()
#
#     @transaction.atomic
#     def tearDown(self):
#         users = User.objects.all()
#         groups = Group.objects.all()
#         for user in users.all():
#             user.delete()
#         for group in groups.all():
#             group.delete()
#         super(TenantIntakeDecoratorWithPublicSchemaTestCase, self).tearDown()
#
#     @transaction.atomic
#     def test_tenant_required_decorator_with_access_denied(self):
#         response = self.authorized_client.get(reverse('tenant_is_valid'))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     # @transaction.atomic
#     # def test_group_is_org_admin_with_failure1(self):
#     #     org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
#     #     self.user.groups.add(org_admin_group)
#     #     self.user.save()
#     #     response = self.authorized_client.get(reverse('group_is_entrepreneur'))
#     #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#     #
#     # @transaction.atomic
#     # def test_group_is_org_admin_with_failure2(self):
#     #     entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
#     #     self.user.groups.add(entrepreneur_group)
#     #     self.user.save()
#     #     response = self.authorized_client.get(reverse('group_is_org_admin'))
#     #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#     #
#     # @transaction.atomic
#     # def test_group_required_with_success(self):
#     #     org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
#     #     entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
#     #     self.user.groups.add(org_admin_group)
#     #     self.user.groups.add(entrepreneur_group)
#     #     self.user.save()
#     #     response = self.authorized_client.get(reverse('group_is_org_admin'))
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     response = self.authorized_client.get(reverse('group_is_entrepreneur'))
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)



class TenantIntakeDecoratorWithTenantSchemaTestCase(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galacticalliance'
        tenant.name = "Galactic Alliance of Humankind"
        tenant.is_setup = True
        tenant.has_perks=True
        tenant.has_mentors=True
        tenant.how_discovered = "Command HQ"
        tenant.how_many_served = 1

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English
        super(TenantIntakeDecoratorWithTenantSchemaTestCase, self).setUp()

        # Initialize our test data.
        Group.objects.bulk_create([
            Group(id=constants.ENTREPRENEUR_GROUP_ID, name="Entreprenuer",),
            Group(id=constants.MENTOR_GROUP_ID, name="Mentor",),
            Group(id=constants.ADVISOR_GROUP_ID, name="Advisor",),
            Group(id=constants.ORGANIZATION_MANAGER_GROUP_ID, name="Org Manager",),
            Group(id=constants.ORGANIZATION_ADMIN_GROUP_ID, name="Org Admin",),
            Group(id=constants.CLIENT_MANAGER_GROUP_ID, name="Client Manager",),
            Group(id=constants.SYSTEM_ADMIN_GROUP_ID, name="System Admin",),
        ])

        self.user = User.objects.create_user(  # Create our User.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD,
            first_name=TEST_USER_FIRSTNAME,
            last_name=TEST_USER_LASTNAME,
        )
        self.user.is_active = True
        self.user.save()
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
        users = User.objects.all()
        groups = Group.objects.all()
        for user in users.all():
            user.delete()
        for group in groups.all():
            group.delete()
        Intake.objects.delete_all()
        # super(TenantIntakeDecoratorWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_tenant_intake_required_decorator_with_access_granted(self):
        # Pre-configure.
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(entrepreneur_group)
        self.user.save()
        me, created = TenantMe.objects.get_or_create(owner=self.user)
        me.is_admitted=True
        me.save()

        # Run our test.
        response = self.authorized_client.get(reverse('tenant_intake_check'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'access-granted',response.content)

    @transaction.atomic
    def test_tenant_intake_required_decorator_with_redirect(self):
        # Pre-configure.
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(entrepreneur_group)
        self.user.save()
        me, created = TenantMe.objects.get_or_create(owner=self.user)
        me.is_admitted=False
        me.save()

        # Run our test and verify.
        response = self.authorized_client.get(reverse('tenant_intake_check'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    @transaction.atomic
    def test_tenant_intake_required_decorator_with_anonymous_user(self):
        # Run our test and verify.
        response = self.unauthorized_client.get(reverse('tenant_intake_check'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    @transaction.atomic
    def test_tenant_intake_has_completed_redirection_required_decorator_with_access_granted(self):
        # Pre-configure.
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(entrepreneur_group)
        self.user.save()
        me, created = TenantMe.objects.get_or_create(owner=self.user)
        me.is_admitted=True
        me.save()

        Intake.objects.create(
            owner=self.user,
            is_completed=False
        )

        # Run our test.
        response = self.authorized_client.get(reverse('tenant_intake_has_completed'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'access-granted',response.content)

    @transaction.atomic
    def test_tenant_intake_has_completed_redirection_required_decorator_with_redirect(self):
        # Pre-configure.
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(entrepreneur_group)
        self.user.save()
        me, created = TenantMe.objects.get_or_create(owner=self.user)
        me.is_admitted=False
        me.save()

        Intake.objects.create(
            owner=self.user,
            is_completed=True
        )

        # Run our test and verify.
        response = self.authorized_client.get(reverse('tenant_intake_check'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    @transaction.atomic
    def test_tenant_intake_has_completed_redirection_required_decorator_with_anonymous_user(self):
        # Run our test and verify.
        response = self.unauthorized_client.get(reverse('tenant_intake_check'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
