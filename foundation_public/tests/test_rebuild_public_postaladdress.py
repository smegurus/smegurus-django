from django.db import transaction
from django.contrib.auth.models import User
from django.utils import translation
from django.core.management import call_command
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_public.models.countryoption import CountryOption
from foundation_public.models.provinceoption import ProvinceOption
from foundation_public.models.postaladdress import PublicPostalAddress
from smegurus.settings import env_var
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRSTNAME = "Ledo"
TEST_USER_LASTNAME = ""


class FoundationPublicRebuildPublicPostalAddressWithPublicSchemaTestCase(TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Public Schema"""
        tenant.schema_name = 'test'
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
        super(FoundationPublicRebuildPublicPostalAddressWithPublicSchemaTestCase, self).setUp()
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
        PublicPostalAddress.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(FoundationPublicRebuildPublicPostalAddressWithPublicSchemaTestCase, self).tearDown()

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
        postal_address = PublicPostalAddress.objects.create(
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
        call_command('rebuild_public_postaladdress',str(postal_address.id))
        postal_address = PublicPostalAddress.objects.get(id=1)
        self.assertTrue(postal_address.latitude != 0)
        self.assertTrue(postal_address.longitude != 0)

        #---------
        # Case 2:
        #---------
        call_command('rebuild_public_postaladdress',str("666"))

        #---------
        # Case 3:
        #---------
        postal_address = PublicPostalAddress.objects.create(
            id=999,
            name='Test Address',
        )
        call_command('rebuild_public_postaladdress',str(postal_address.id))
