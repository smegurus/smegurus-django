from django.db import transaction
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import resolve, reverse
from django.utils import translation
from django.core.management import call_command
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_tenant.models.base.me import TenantMe
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.contactpoint import ContactPoint
from foundation_tenant.models.base.countryoption import CountryOption
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRSTNAME = "Ledo"
TEST_USER_LASTNAME = ""


class FoundationTenantUtilsWithTenantSchemaTestCase(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Public Schema"""
        tenant.schema_name = 'galacticallianceofhumankind'
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

    @transaction.atomic
    def setUp(self):
        super(FoundationTenantUtilsWithTenantSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        CountryOption.objects.delete_all()
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        TenantMe.objects.delete_all()
        items = User.objects.all()
        for item in items.all():
            item.delete()
        # super(FoundationTenantUtilsWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_populate_countries_for_this_tenant(self):
        call_command('populate_tenant')
        countries_count = CountryOption.objects.count()
        self.assertEqual(countries_count, 3)
