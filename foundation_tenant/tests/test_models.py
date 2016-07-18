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
from foundation_tenant.models.me import TenantMe
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
        tenant.schema_name = 'galacticalliance'
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
        User.objects.bulk_create([
            User(email='1@1.com', username='1',password='1',is_active=True,),
            User(email='2@2.com', username='2',password='2',is_active=True,),
            User(email='3@3.com', username='3',password='3',is_active=True,),
            User(email='4@4.com', username='4',password='4',is_active=True,),
            User(email='5@5.com', username='5',password='5',is_active=True,),
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
    def test_place_to_string(self):
        obj = Place.objects.create(
            name='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete();  # Cleanup

    @transaction.atomic
    def test_place_delete_all(self):
        # Setup our unit test.
        count = Place.objects.all().count()
        self.assertEqual(count, 0)
        Place.objects.bulk_create([
            Place(name='Transhumanism',),
            Place(name='Space exploration',),
            Place(name='Unlimited energy',),
            Place(name='Defend hive',),
        ])
        count = Place.objects.all().count()
        self.assertEqual(count, 4)

        # Run our test and verify.
        Place.objects.delete_all()
        count = Place.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        for item in Place.objects.all():
            item.delete()

    @transaction.atomic
    def test_postaladdress_to_string(self):
        obj = PostalAddress.objects.create(
            name='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')

    @transaction.atomic
    def test_postaladdress_delete_all(self):
        # Setup our unit test.
        count = PostalAddress.objects.all().count()
        self.assertEqual(count, 0)
        PostalAddress.objects.bulk_create([
            PostalAddress(name='Transhumanism',),
            PostalAddress(name='Space exploration',),
            PostalAddress(name='Unlimited energy',),
            PostalAddress(name='Defend hive',),
        ])
        count = PostalAddress.objects.all().count()
        self.assertEqual(count, 4)

        # Run our test and verify.
        PostalAddress.objects.delete_all()
        count = PostalAddress.objects.all().count()
        self.assertEqual(count, 0)

    @transaction.atomic
    def test_businessidea_to_string(self):
        obj = BusinessIdea.objects.create(
            name='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete()

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
        self.assertEqual(count, 4)

        # Run our test and verify.
        BusinessIdea.objects.delete_all()
        count = BusinessIdea.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        items = BusinessIdea.objects.all()
        for item in items.all():
            item.delete()

    @transaction.atomic
    def test_tellusyourneed_to_string(self):
        obj = TellUsYourNeed.objects.create(
            id=2030,
            owner=User.objects.get(username='1')
        )
        self.assertIn(str(obj), '2030')
        obj.delete()

    @transaction.atomic
    def test_tellusyourneed_delete_all(self):
        # Setup our unit test.
        count = TellUsYourNeed.objects.all().count()
        self.assertEqual(count, 0)
        TellUsYourNeed.objects.bulk_create([
            TellUsYourNeed(id=1, owner=User.objects.get(username='1')),
            TellUsYourNeed(id=2, owner=User.objects.get(username='2')),
            TellUsYourNeed(id=3, owner=User.objects.get(username='3')),
            TellUsYourNeed(id=4, owner=User.objects.get(username='4')),
            TellUsYourNeed(id=5, owner=User.objects.get(username='5')),
        ])
        count = TellUsYourNeed.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        TellUsYourNeed.objects.delete_all()
        count = TellUsYourNeed.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        items = TellUsYourNeed.objects.all()
        for item in items.all():
            item.delete()

    @transaction.atomic
    def test_tag_to_string(self):
        obj = Tag.objects.create(
            name='Testing',
        )
        self.assertIn(str(obj), 'Testing')
        obj.delete()

    @transaction.atomic
    def test_tag_delete_all(self):
        # Setup our unit test.
        count = Tag.objects.all().count()
        self.assertEqual(count, 0)
        Tag.objects.bulk_create([
            Tag(id=1, name='1'),
            Tag(id=2, name='2'),
            Tag(id=3, name='3'),
            Tag(id=4, name='4'),
            Tag(id=5, name='5'),
        ])
        count = Tag.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        Tag.objects.delete_all()
        count = Tag.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        items = Tag.objects.all()
        for item in items.all():
            item.delete()

    @transaction.atomic
    def test_openinghoursspecification_to_string(self):
        obj = OpeningHoursSpecification.objects.create(
            name='Testing',
        )
        self.assertIn(str(obj), 'Testing')
        obj.delete()

    @transaction.atomic
    def test_openinghoursspecification_delete_all(self):
        # Setup our unit test.
        count = OpeningHoursSpecification.objects.all().count()
        self.assertEqual(count, 0)
        OpeningHoursSpecification.objects.bulk_create([
            OpeningHoursSpecification(id=1, name='1', owner=User.objects.get(username='1')),
            OpeningHoursSpecification(id=2, name='2', owner=User.objects.get(username='2')),
            OpeningHoursSpecification(id=3, name='3', owner=User.objects.get(username='3')),
            OpeningHoursSpecification(id=4, name='4', owner=User.objects.get(username='4')),
            OpeningHoursSpecification(id=5, name='5', owner=User.objects.get(username='5')),
        ])
        count = OpeningHoursSpecification.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        OpeningHoursSpecification.objects.delete_all()
        count = OpeningHoursSpecification.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        items = OpeningHoursSpecification.objects.all()
        for item in items.all():
            item.delete()

    @transaction.atomic
    def test_tenant_me_to_string(self):
        obj = TenantMe.objects.create(
            id=1,
            owner=User.objects.get(username='1'),
        )
        self.assertIn(str(obj), '1')
        obj.delete()

    @transaction.atomic
    def test_tenant_get_by_owner_or_none_with_success(self):
        user = User.objects.get(username='1')
        TenantMe.objects.create(
            id=999,
            owner=user,
        )
        me = TenantMe.objects.get_by_owner_or_none(owner=user)
        self.assertIsNotNone(me)
        me.delete()

    @transaction.atomic
    def test_tenant_get_by_owner_or_none_with_none(self):
        target_me = TenantMe.objects.create(
            id=666,
            owner=User.objects.get(username='1'),
        )
        search_me = TenantMe.objects.get_by_owner_or_none(owner=User.objects.get(username='2'))
        self.assertIsNone(search_me)
        target_me.delete()

    @transaction.atomic
    def test_tenant_me_delete_all(self):
        # Setup our unit test.
        count = TenantMe.objects.all().count()
        self.assertEqual(count, 0)
        TenantMe.objects.bulk_create([
            TenantMe(id=1, owner=User.objects.get(username='1')),
            TenantMe(id=2, owner=User.objects.get(username='2')),
            TenantMe(id=3, owner=User.objects.get(username='3')),
            TenantMe(id=4, owner=User.objects.get(username='4')),
            TenantMe(id=5, owner=User.objects.get(username='5')),
        ])
        count = TenantMe.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        TenantMe.objects.delete_all()
        count = TenantMe.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        items = TenantMe.objects.all()
        for item in items.all():
            item.delete()
