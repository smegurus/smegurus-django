from django.core import mail
from django.core.signing import Signer
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework.test import APITestCase
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_tenant.models.fileupload import TenantFileUpload
from foundation_tenant.models.imageupload import TenantImageUpload
from foundation_tenant.models.abstract_creativework import AbstractCreativeWork
from foundation_tenant.models.abstract_mediaobject import AbstractMediaObject
from foundation_tenant.models.language import Language
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.openinghoursspecification import OpeningHoursSpecification
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.geocoordinate import GeoCoordinate
from foundation_tenant.models.abstract_place import AbstractPlace
from foundation_tenant.models.country import Country
from foundation_tenant.models.abstract_intangible import AbstractIntangible
from foundation_tenant.models.brand import Brand
from foundation_tenant.models.place import Place
from foundation_tenant.models.abstract_person import AbstractPerson
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.businessidea import BusinessIdea
from foundation_tenant.models.tellusyourneed import TellUsYourNeed

from foundation_public import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRST_NAME = "Ledo"
TEST_USER_LAST_NAME = ""


class FoundationTenantModelsWithTenantSchemaTestCases(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Public Schema"""
        tenant.schema_name = 'test'
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

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English
        super(FoundationTenantModelsWithTenantSchemaTestCases, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(FoundationTenantModelsWithTenantSchemaTestCases, self).tearDown()

    @transaction.atomic
    def test_businessidea_to_string(self):
        obj = BusinessIdea.objects.create(
            name='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')

    @transaction.atomic
    def test_businessidea_delete_all(self):
        # Setup our unit test.
        count = BusinessIdea.objects.all().count()
        self.assertEqual(count, 0)
        BusinessIdea.objects.bulk_create([
            BusinessIdea(name='Transhumanism',),
            BusinessIdea(name='Space exploration',),
            BusinessIdea(name='Unlimited energy',),
            BusinessIdea(name='Defend hive',),
        ])
        count = BusinessIdea.objects.all().count()
        self.assertEqual(count, 3)

        # Run our test and verify.
        BusinessIdea.objects.delete_all()
        count = BusinessIdea.objects.all().count()
        self.assertEqual(count, 0)
