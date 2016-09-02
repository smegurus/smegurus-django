from django.core import mail
from django.core.signing import Signer
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework.test import APITestCase
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from smegurus import constants
from foundation_public.models.banned import BannedDomain
from foundation_public.models.banned import BannedIP
from foundation_public.models.banned import BannedWord
from foundation_public.models.fileupload import PublicFileUpload
from foundation_public.models.imageupload import PublicImageUpload
from foundation_public.models.abstract_thing import AbstractPublicThing
from foundation_public.models.brand import PublicBrand
from foundation_public.models.contactpoint import PublicContactPoint
from foundation_public.models.geocoordinate import PublicGeoCoordinate
from foundation_public.models.language import PublicLanguage
from foundation_public.models.openinghoursspecification import PublicOpeningHoursSpecification
from foundation_public.models.postaladdress import PublicPostalAddress
from foundation_public.models.place import PublicPlace
from foundation_public.models.country import PublicCountry
from foundation_public.models.abstract_person import AbstractPlacePerson
from foundation_public.models.organization import PublicOrganization
from foundation_public.models.organization import PublicDomain
from foundation_public.models.visitor import PublicVisitor


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRST_NAME = "Ledo"
TEST_USER_LAST_NAME = ""


class FoundationPublicModelsWithPublicSchemaTestCases(APITestCase, TenantTestCase):
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
        translation.activate('en')  # Set English
        super(FoundationPublicModelsWithPublicSchemaTestCases, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        pass
        # users = User.objects.all()
        # for user in users.all():
        #     user.delete()
        # super(FoundationPublicModelsWithPublicSchemaTestCases, self).tearDown()

    @transaction.atomic
    def test_banned_domain_to_string(self):
        obj = BannedDomain.objects.create(
            name='hideauze.com',
            reason='Enemy of Humankind',
        )
        self.assertIn(str(obj), 'hideauze.com')

    @transaction.atomic
    def test_banned_ip_to_string(self):
        obj = BannedIP.objects.create(
            address='127.0.0.1',
            reason='Enemy of Humankind',
        )
        self.assertIn(str(obj), '127.0.0.1')

    @transaction.atomic
    def test_banned_word_to_string(self):
        obj = BannedWord.objects.create(
            text='Ghost',
            reason='Lowers moral of soldiers',
        )
        self.assertIn(str(obj), 'Ghost')

    @transaction.atomic
    def test_country_to_string(self):
        obj = PublicCountry.objects.create(
            name='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')

    # @transaction.atomic
    # def test_fileupload_to_string(self):
    #     pass
    #
    # @transaction.atomic
    # def test_imageupload_to_string(self):
    #     pass

    @transaction.atomic
    def test_brand_to_string(self):
        obj = PublicBrand.objects.create(
            name='Chambers',
        )
        self.assertIn(str(obj), 'Chambers')

    @transaction.atomic
    def test_contactpoint_to_string(self):
        obj = PublicContactPoint.objects.create(
            name='Chambers',
        )
        self.assertIn(str(obj), 'Chambers')

    @transaction.atomic
    def test_geocoordinate_to_string(self):
        obj = PublicGeoCoordinate.objects.create(
            name='Chambers',
        )
        self.assertIn(str(obj), 'Chambers')

    @transaction.atomic
    def test_language_to_string(self):
        obj = PublicLanguage.objects.create(
            name='Chambers',
        )
        self.assertIn(str(obj), 'Chambers')

    @transaction.atomic
    def test_openinghoursspecification_to_string(self):
        obj = PublicOpeningHoursSpecification.objects.create(
            name='Chambers',
        )
        self.assertIn(str(obj), 'Chambers')

    @transaction.atomic
    def test_postaladdress_to_string(self):
        obj = PublicPostalAddress.objects.create(
            name='Chambers',
        )
        self.assertIn(str(obj), 'Chambers')

    @transaction.atomic
    def test_postaladdress_delete_all(self):
        PublicPostalAddress.objects.create(
            name='Chambers',
        )
        PublicPostalAddress.objects.delete_all()
        count = PublicPostalAddress.objects.count()
        self.assertEqual(count, 1)

    @transaction.atomic
    def test_place_to_string(self):
        obj = PublicPlace.objects.create(
            name='Chambers',
        )
        self.assertIn(str(obj), 'Chambers')

    @transaction.atomic
    def test_organization_to_string(self):
        self.assertIn(str(self.tenant), "Galactic Alliance of Humankind")

    @transaction.atomic
    def test_public_visitor_to_string(self):
        vistor = PublicVisitor.objects.create(
            id=1,
            path="/en/",
            ip_address="127.0.0.1"
        )
        self.assertIn('/en/ by 127.0.0.1', str(vistor))
        vistor.delete();  # Cleanup

    @transaction.atomic
    def test_public_visitor_delete_all(self):
        # Setup our unit test.
        count = PublicVisitor.objects.all().count()
        self.assertEqual(count, 0)
        PublicVisitor.objects.bulk_create([
            PublicVisitor(
                id = 1111,
                path="/en/",
                ip_address="127.0.0.1"
            ),
            PublicVisitor(
                id = 2222,
                path="/en/",
                ip_address="127.0.0.1"
            ),
            PublicVisitor(
                id = 3333,
                path="/en/",
                ip_address="127.0.0.1"
            ),
            PublicVisitor(
                id = 4444,
                path="/en/",
                ip_address="127.0.0.1"
            ),
            PublicVisitor(
                id = 5555,
                path="/en/",
                ip_address="127.0.0.1"
            ),
        ])
        count = PublicVisitor.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        Visitor.objects.delete_all()
        count = PublicVisitor.objects.all().count()
        self.assertEqual(count, 0)

    @transaction.atomic
    def test_public_visitor_is_path_suspicious(self):
        # CASE 1 OF 2:
        vistor = PublicVisitor.objects.create(
            id=1,
            path="/HNAP1/",
            ip_address="127.0.0.1"
        )
        self.assertTrue(vistor.is_path_suspicious())
        vistor.delete();  # Cleanup

        # CASE 2 OF 2:
        vistor = PublicVisitor.objects.create(
            id=1,
            path="/en/",
            ip_address="127.0.0.1"
        )
        self.assertFalse(vistor.is_path_suspicious())
        vistor.delete();  # Cleanup
