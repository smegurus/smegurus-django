from django.db import transaction
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import resolve, reverse
from django.utils import translation
from django.core.management import call_command
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.countryoption import CountryOption
from foundation_tenant.models.provinceoption import ProvinceOption
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRSTNAME = "Ledo"
TEST_USER_LASTNAME = ""


class FoundationTenantRebuildTenantPostalAddressWithTenantSchemaTestCase(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
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
        super(FoundationTenantRebuildTenantPostalAddressWithTenantSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)
        self.user = User.objects.create_user(  # Create our User.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD,
            first_name=TEST_USER_FIRSTNAME,
            last_name=TEST_USER_LASTNAME
        )
        self.user.is_active = True
        self.user.save()


    @transaction.atomic
    def tearDown(self):
        CountryOption.objects.delete_all()
        ProvinceOption.objects.delete_all()
        PostalAddress.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(FoundationTenantRebuildTenantPostalAddressWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_command(self):
        #---------
        # Case 1:
        #---------
        # Create a new object with our specific test data.
        country = CountryOption.objects.create(
            id=1,
            name='Ontario',
        )
        region = ProvinceOption.objects.create(
            id=1,
            name='Canada',
            country=country
        )
        postal_address = PostalAddress.objects.create(
            id=1,
            name='Test Address',
            owner=self.user,
            street_number='120',
            street_name='Centre Street',
            suite_number='102',
            postal_code='N6J4X4',
            locality='London',
            region=region,
            country=country,
        )

        # Run the command and verify.
        call_command('rebuild_tenant_postaladdress',str(postal_address.id))
        postal_address = PostalAddress.objects.get(id=1)
        self.assertTrue(postal_address.latitude != 0)
        self.assertTrue(postal_address.longitude != 0)

        #---------
        # Case 2:
        #---------
        call_command('rebuild_tenant_postaladdress',str("666"))

        #---------
        # Case 3:
        #---------
        postal_address = PostalAddress.objects.create(
            id=999,
            name='Test Address',
        )
        call_command('rebuild_tenant_postaladdress',str(postal_address.id))
