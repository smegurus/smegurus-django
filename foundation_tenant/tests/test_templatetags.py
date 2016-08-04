from django.db import transaction
from django.contrib.auth.models import User, Group
from django.utils import translation
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from rest_framework.test import APITestCase
from foundation_tenant.templatetags.foundation_tenant_tags import is_employee
from foundation_tenant.models.me import TenantMe
from foundation_public.models.organization import PublicOrganization, PublicDomain
from foundation_public import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRSTNAME = "Ledo"
TEST_USER_LASTNAME = ""


class FoundationTenantTemplateTagsWithTenantSchemaTestCase(APITestCase, TenantTestCase):
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
            password=TEST_USER_PASSWORD,
            first_name=TEST_USER_FIRSTNAME,
            last_name=TEST_USER_LASTNAME,
        )
        user.is_active = True
        user.save()

    @transaction.atomic
    def setUp(self):
        super(FoundationTenantTemplateTagsWithTenantSchemaTestCase, self).setUp()
        self.user = User.objects.get()

    @transaction.atomic
    def tearDown(self):
        items = Group.objects.all()
        for item in items.all():
            item.delete()
        items = User.objects.all()
        for item in items.all():
            item.delete()
        TenantMe.objects.delete_all()
        # super(FoundationTenantTemplateTagsWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_me_is_employee_is_employee(self):
        # Grant our User a employee role.
        group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.add(group)
        self.user.save()

        # Create our employee.
        me = TenantMe.objects.create(
            owner=self.user,
        )

        # Run unit-test and verify.
        value = is_employee(me)
        self.assertTrue(value)

    @transaction.atomic
    def test_me_is_employee_is_entrepreneur(self):
        # Grant our User a employee role.
        group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(group)
        self.user.save()

        # Create our employee.
        me = TenantMe.objects.create(
            owner=self.user,
        )

        # Run unit-test and verify.
        value = is_employee(me)
        self.assertFalse(value)
