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
from foundation_tenant.models.calendarevent import CalendarEvent
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.admission import Admission
from foundation_tenant.models.faqitem import FAQItem
from foundation_tenant.models.faqgroup import FAQGroup
from foundation_tenant.models.communitypost import CommunityPost
from foundation_tenant.models.communityadvertisement import CommunityAdvertisement
from foundation_tenant.models.message import Message
from foundation_tenant.models.note import Note
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.orderedlogevent import OrderedLogEvent
from foundation_tenant.models.orderedcommentpost import OrderedCommentPost
from foundation_tenant.models.task import Task
from foundation_tenant.models.countryoption import CountryOption
from foundation_tenant.models.provinceoption import ProvinceOption
from foundation_tenant.models.cityoption import CityOption
from foundation_tenant.models.visitor import TenantVisitor


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
        items = User.objects.all()
        for item in items.all():
            item.delete()
        items = Group.objects.all()
        for item in items.all():
            item.delete()
        # super(FoundationTenantModelsWithTenantSchemaTestCases, self).tearDown()

    @transaction.atomic
    def test_intake_to_string(self):
        me = TenantMe.objects.create(
            id=1,
            owner=User.objects.get(username='1'),
            name='Ice Age',
        )
        obj = Intake.objects.create(
            id=1,
            me=me
        )
        self.assertIn(str(obj), 'Ice Age')
        obj.delete();  # Cleanup
        me.delete()

    @transaction.atomic
    def test_intake_delete_all(self):
        # Setup our unit test.
        count = Intake.objects.all().count()
        self.assertEqual(count, 0)
        Intake.objects.bulk_create([
            Intake(
                id = 1111,
                me=TenantMe.objects.create(
                    id = 1111,
                    owner=User.objects.get(username='1')
                )
            ),
            Intake(
                id = 2222,
                me = TenantMe.objects.create(
                    id = 1112,
                    owner=User.objects.get(username='1'),
                )
            ),
            Intake(
                id = 3333,
                me = TenantMe.objects.create(
                    id = 1113,
                    owner=User.objects.get(username='1'),
                )
            ),
            Intake(
                id = 4444,
                me = TenantMe.objects.create(
                    id = 1114,
                    owner=User.objects.get(username='1'),
                )
            ),
            Intake(
                id = 5555,
                me = TenantMe.objects.create(
                    id = 1115,
                    owner=User.objects.get(username='1'),
                )
            ),
        ])
        count = Intake.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        Intake.objects.delete_all()
        count = Intake.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        TenantMe.objects.delete_all()

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
    def test_tenant_me_is_entrepreneur_with_false(self):
        # Attach non-entrepreneur group.
        group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        user = User.objects.get(username='1')
        user.groups.add(group)
        obj = TenantMe.objects.create(
            id=1,
            owner=user,
        )

        # Run the test and verify.
        self.assertFalse(obj.is_entrepreneur())
        obj.delete()

    @transaction.atomic
    def test_tenant_me_is_entrepreneur_with_true(self):
        # Attach entrepreneur group.
        group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        user = User.objects.get(username='1')
        user.groups.add(group)
        obj = TenantMe.objects.create(
            id=1,
            owner=user,
        )

        # Run the test and verify
        self.assertTrue(obj.is_entrepreneur())
        obj.delete()

    @transaction.atomic
    def test_tenant_me_is_employee_with_true(self):
        # Attach employee group.
        group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        user = User.objects.get(username='1')
        user.groups.add(group)
        obj = TenantMe.objects.create(
            id=1,
            owner=user,
        )

        # Run the test and verify
        self.assertTrue(obj.is_employee())
        obj.delete()

    @transaction.atomic
    def test_tenant_me_is_employee_with_false(self):
        # Attach non-employee group.
        group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        user = User.objects.get(username='1')
        user.groups.add(group)
        obj = TenantMe.objects.create(
            id=1,
            owner=user,
        )

        # Run the test and verify
        self.assertFalse(obj.is_employee())
        obj.delete()

    @transaction.atomic
    def test_tenant_me_is_manager_with_true(self):
        # Attach manager group.
        group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        user = User.objects.get(username='1')
        user.groups.add(group)
        obj = TenantMe.objects.create(
            id=1,
            owner=user,
        )

        # Run the test and verify
        self.assertTrue(obj.is_manager())
        obj.delete()

    @transaction.atomic
    def test_tenant_me_is_manager_with_false(self):
        # Attach non-manager group.
        group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        user = User.objects.get(username='1')
        user.groups.add(group)
        obj = TenantMe.objects.create(
            id=1,
            owner=user,
        )

        # Run the test and verify
        self.assertFalse(obj.is_manager())
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
    def test_tenant_me_get_by_owner_or_none_with_none(self):
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

    @transaction.atomic
    def test_calendar_event_get_by_owner_or_none_with_none(self):
        target_me = TenantMe.objects.create(
            id=666,
            owner=User.objects.get(username='1'),
        )
        search_me = TenantMe.objects.get_by_owner_or_none(owner=User.objects.get(username='2'))
        self.assertIsNone(search_me)
        target_me.delete()

    @transaction.atomic
    def test_calendar_event_delete_all(self):
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

    @transaction.atomic
    def test_admission_to_string(self):
        tag = Tag.objects.create(
            name='Testing',
        )
        self.assertIn(str(tag), 'Testing')
        admission = Admission.objects.create(
            tag=tag,
        )
        self.assertIn(str(admission), 'Testing')
        admission.delete();  # Cleanup
        tag.delete()

    @transaction.atomic
    def test_admission_delete_all(self):
        # Setup our unit test.
        count = Place.objects.all().count()
        self.assertEqual(count, 0)
        tag = Tag.objects.create(
            name='Testing',
        )
        self.assertIn(str(tag), 'Testing')
        admission = Admission.objects.create(
            tag=tag,
        )
        count = Admission.objects.all().count()
        self.assertEqual(count, 1)

        # Run our test and verify.
        Admission.objects.delete_all()
        count = Admission.objects.all().count()
        self.assertEqual(count, 0)

    @transaction.atomic
    def test_faqgroup_to_string(self):
        obj = FAQGroup.objects.create(
            text='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete();  # Cleanup

    @transaction.atomic
    def test_faqgroup_delete_all(self):
        # Setup our unit test.
        count = FAQGroup.objects.all().count()
        self.assertEqual(count, 0)
        FAQGroup.objects.create(
            text='hideauze.com',
        )
        count = FAQGroup.objects.all().count()
        self.assertEqual(count, 1)

        # Run our test and verify.
        FAQGroup.objects.delete_all()
        count = FAQItem.objects.all().count()
        self.assertEqual(count, 0)

    @transaction.atomic
    def test_faqitem_to_string(self):
        obj = FAQItem.objects.create(
            question_text='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete();  # Cleanup

    @transaction.atomic
    def test_faqitem_delete_all(self):
        # Setup our unit test.
        count = FAQItem.objects.all().count()
        self.assertEqual(count, 0)
        FAQItem.objects.create(
            question_text='hideauze.com',
        )
        count = FAQItem.objects.all().count()
        self.assertEqual(count, 1)

        # Run our test and verify.
        FAQItem.objects.delete_all()
        count = FAQItem.objects.all().count()
        self.assertEqual(count, 0)

    @transaction.atomic
    def test_communitypost_to_string(self):
        obj = CommunityPost.objects.create(
            name='hideauze.com',
            owner=User.objects.get(username='1')
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete();  # Cleanup

    @transaction.atomic
    def test_communitypost_delete_all(self):
        # Setup our unit test.
        count = CommunityPost.objects.all().count()
        self.assertEqual(count, 0)
        CommunityPost.objects.create(
            name='Testing',
            owner=User.objects.get(username='1'),
        )
        count = CommunityPost.objects.all().count()
        self.assertEqual(count, 1)

        # Run our test and verify.
        CommunityPost.objects.delete_all()
        count = CommunityPost.objects.all().count()
        self.assertEqual(count, 0)

    @transaction.atomic
    def test_communityadvertisement_to_string(self):
        obj = CommunityAdvertisement.objects.create(
            name='hideauze.com',
            owner=User.objects.get(username='1')
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete();  # Cleanup

    @transaction.atomic
    def test_communityadvertisement_delete_all(self):
        # Setup our unit test.
        count = CommunityAdvertisement.objects.all().count()
        self.assertEqual(count, 0)
        CommunityAdvertisement.objects.create(
            name='Testing',
            owner=User.objects.get(username='1'),
        )
        count = CommunityAdvertisement.objects.all().count()
        self.assertEqual(count, 1)

        # Run our test and verify.
        CommunityAdvertisement.objects.delete_all()
        count = CommunityAdvertisement.objects.all().count()
        self.assertEqual(count, 0)

    @transaction.atomic
    def test_message_to_string(self):
        obj = Message.objects.create(
            name='hideauze.com',
            owner=User.objects.get(username='1')
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete();  # Cleanup

    @transaction.atomic
    def test_message_delete_all(self):
        # Setup our unit test.
        count = Message.objects.all().count()
        self.assertEqual(count, 0)
        Message.objects.create(
            name='Testing',
            owner=User.objects.get(username='1'),
        )
        count = Message.objects.all().count()
        self.assertEqual(count, 1)

        # Run our test and verify.
        Message.objects.delete_all()
        count = Message.objects.all().count()
        self.assertEqual(count, 0)

    @transaction.atomic
    def test_entrepreneur_note_to_string(self):
        me = TenantMe.objects.create(
            id=1,
            owner=User.objects.get(username='1'),
            name='Ice Age',
        )
        obj = Note.objects.create(
            id=1,
            me=me
        )
        self.assertIn(str(obj), 'Ice Age')
        obj.delete();  # Cleanup
        me.delete()

    @transaction.atomic
    def test_entrepreneur_note_delete_all(self):
        # Setup our unit test.
        count = Note.objects.all().count()
        self.assertEqual(count, 0)
        Note.objects.bulk_create([
            Note(
                id = 1111,
                me=TenantMe.objects.create(
                    id = 1111,
                    owner=User.objects.get(username='1')
                )
            ),
            Note(
                id = 2222,
                me = TenantMe.objects.create(
                    id = 1112,
                    owner=User.objects.get(username='1'),
                )
            ),
            Note(
                id = 3333,
                me = TenantMe.objects.create(
                    id = 1113,
                    owner=User.objects.get(username='1'),
                )
            ),
            Note(
                id = 4444,
                me = TenantMe.objects.create(
                    id = 1114,
                    owner=User.objects.get(username='1'),
                )
            ),
            Note(
                id = 5555,
                me = TenantMe.objects.create(
                    id = 1115,
                    owner=User.objects.get(username='1'),
                )
            ),
        ])
        count = Note.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        Note.objects.delete_all()
        count = Note.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        TenantMe.objects.delete_all()

    @transaction.atomic
    def test_ordered_log_event_to_string(self):
        me = TenantM.objects.create(
            id=1,
            owner=User.objects.get(username='1'),
            name='Ice Age',
        )
        obj = OrderedLogEvent.objects.create(
            id=1,
            me=me,
            text="Ice Age"
        )
        self.assertIn(str(obj), 'Ice Age')
        obj.delete();  # Cleanup
        me.delete()

    @transaction.atomic
    def test_ordered_log_event_delete_all(self):
        # Setup our unit test.
        count = OrderedLogEvent.objects.all().count()
        self.assertEqual(count, 0)
        OrderedLogEvent.objects.bulk_create([
            OrderedLogEvent(
                id = 1111,
                me=TenantMe.objects.create(
                    id = 1111,
                    owner=User.objects.get(username='1')
                ),
                text="Ice Age"
            ),
            OrderedLogEvent(
                id = 2222,
                me = TenantMe.objects.create(
                    id = 1112,
                    owner=User.objects.get(username='1'),
                ),
                text="Global Cooling"
            ),
            OrderedLogEvent(
                id = 3333,
                me = TenantMe.objects.create(
                    id = 1113,
                    owner=User.objects.get(username='1'),
                ),
                text="Solar Hibernation"
            ),
            OrderedLogEvent(
                id = 4444,
                me = TenantMe.objects.create(
                    id = 1114,
                    owner=User.objects.get(username='1'),
                ),
                text="Mini-Ice Age"
            ),
            OrderedLogEvent(
                id = 5555,
                me = TenantMe.objects.create(
                    id = 1115,
                    owner=User.objects.get(username='1'),
                ),
                text="Solar Reflective Particles"
            ),
        ])
        count = OrderedLogEvent.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        OrderedLogEvent.objects.delete_all()
        count = OrderedLogEvent.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        TenantMe.objects.delete_all()

    @transaction.atomic
    def test_ordered_comment_post_to_string(self):
        me = TenantM.objects.create(
            id=1,
            owner=User.objects.get(username='1'),
            name='Ice Age',
        )
        obj = OrderedCommentPost.objects.create(
            id=1,
            me=me,
            description="Ice Age"
        )
        self.assertIn(str(obj), 'Ice Age')
        obj.delete();  # Cleanup
        me.delete()

    @transaction.atomic
    def test_ordered_log_event_delete_all(self):
        # Setup our unit test.
        count = OrderedCommentPost.objects.all().count()
        self.assertEqual(count, 0)
        OrderedCommentPost.objects.bulk_create([
            OrderedCommentPost(
                id = 1111,
                me=TenantMe.objects.create(
                    id = 1111,
                    owner=User.objects.get(username='1')
                ),
                description="Ice Age"
            ),
            OrderedCommentPost(
                id = 2222,
                me = TenantMe.objects.create(
                    id = 1112,
                    owner=User.objects.get(username='1'),
                ),
                description="Global Cooling"
            ),
            OrderedCommentPost(
                id = 3333,
                me = TenantMe.objects.create(
                    id = 1113,
                    owner=User.objects.get(username='1'),
                ),
                description="Solar Hibernation"
            ),
            OrderedCommentPost(
                id = 4444,
                me = TenantMe.objects.create(
                    id = 1114,
                    owner=User.objects.get(username='1'),
                ),
                description="Mini-Ice Age"
            ),
            OrderedCommentPost(
                id = 5555,
                me = TenantMe.objects.create(
                    id = 1115,
                    owner=User.objects.get(username='1'),
                ),
                description="Solar Reflective Particles"
            ),
        ])
        count = OrderedCommentPost.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        OrderedCommentPost.objects.delete_all()
        count = OrderedLogEvent.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        TenantMe.objects.delete_all()

    @transaction.atomic
    def test_task_to_string(self):
        me = TenantMe.objects.create(
            id=1,
            owner=User.objects.get(username='1'),
            name='Ice Age',
        )
        obj = Task.objects.create(
            id=1,
            assigned_by=me,
            description="Ice Age"
        )
        self.assertIn(str(obj), 'Ice Age')
        obj.delete();  # Cleanup
        me.delete()

    @transaction.atomic
    def test_task_delete_all(self):
        # Setup our unit test.
        count = Task.objects.all().count()
        self.assertEqual(count, 0)
        Task.objects.bulk_create([
            Task(
                id = 1111,
                assigned_by=TenantMe.objects.create(
                    id = 1111,
                    owner=User.objects.get(username='1')
                ),
                description="Ice Age"
            ),
            Task(
                id = 2222,
                assigned_by = TenantMe.objects.create(
                    id = 1112,
                    owner=User.objects.get(username='1'),
                ),
                description="Global Cooling"
            ),
            Task(
                id = 3333,
                assigned_by = TenantMe.objects.create(
                    id = 1113,
                    owner=User.objects.get(username='1'),
                ),
                description="Solar Hibernation"
            ),
            Task(
                id = 4444,
                assigned_by = TenantMe.objects.create(
                    id = 1114,
                    owner=User.objects.get(username='1'),
                ),
                description="Mini-Ice Age"
            ),
            Task(
                id = 5555,
                assigned_by = TenantMe.objects.create(
                    id = 1115,
                    owner=User.objects.get(username='1'),
                ),
                description="Solar Reflective Particles"
            ),
        ])
        count = Task.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        Task.objects.delete_all()
        count = Task.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        TenantMe.objects.delete_all()

    @transaction.atomic
    def test_task_get_absolute_url(self):
        me = TenantMe.objects.create(
            id=1,
            owner=User.objects.get(username='1'),
            name='Ice Age',
        )
        obj = Task.objects.create(
            id=666,
            assigned_by=me,
            description="Ice Age"
        )
        self.assertIn(obj.get_absolute_url(), '/en/task/666/')
        obj.delete();  # Cleanup
        me.delete()

    @transaction.atomic
    def test_tenant_visitor_to_string_by_user(self):
        vistor = TenantVisitor.objects.create(
            id=1,
            me=TenantMe.objects.create(
                id = 1111,
                owner=User.objects.get(username='1'),
                name="Ledo"
            ),
            path="/en/",
            ip_address="127.0.0.1"
        )
        self.assertIn('/en/ by Ledo', str(vistor))
        vistor.delete();  # Cleanup

    @transaction.atomic
    def test_tenant_visitor_delete_all(self):
        # Setup our unit test.
        count = TenantVisitor.objects.all().count()
        self.assertEqual(count, 0)
        TenantVisitor.objects.bulk_create([
            TenantVisitor(
                id = 1111,
                me=TenantMe.objects.create(
                    id = 1111,
                    owner=User.objects.get(username='1')
                ),
                path="/en/",
                ip_address="127.0.0.1"
            ),
            TenantVisitor(
                id = 2222,
                me = TenantMe.objects.create(
                    id = 1112,
                    owner=User.objects.get(username='1'),
                ),
                path="/en/",
                ip_address="127.0.0.1"
            ),
            TenantVisitor(
                id = 3333,
                me = TenantMe.objects.create(
                    id = 1113,
                    owner=User.objects.get(username='1'),
                ),
                path="/en/",
                ip_address="127.0.0.1"
            ),
            TenantVisitor(
                id = 4444,
                me = TenantMe.objects.create(
                    id = 1114,
                    owner=User.objects.get(username='1'),
                ),
                path="/en/",
                ip_address="127.0.0.1"
            ),
            TenantVisitor(
                id = 5555,
                me = TenantMe.objects.create(
                    id = 1115,
                    owner=User.objects.get(username='1'),
                ),
                path="/en/",
                ip_address="127.0.0.1"
            ),
        ])
        count = TenantVisitor.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        TenantVisitor.objects.delete_all()
        count = TenantVisitor.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        TenantMe.objects.delete_all()
