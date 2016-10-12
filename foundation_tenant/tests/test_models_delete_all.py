from django.core import mail
from django.core.signing import Signer
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework.test import APITestCase
from tenant_schemas.test.cases import TenantTestCase
from tenant_schemas.test.client import TenantClient
from smegurus import constants
from foundation_tenant.models.fileupload import TenantFileUpload
from foundation_tenant.models.imageupload import TenantImageUpload
from foundation_tenant.models.governmentbenefitoption import GovernmentBenefitOption
from foundation_tenant.models.identifyoption import IdentifyOption
from foundation_tenant.models.language import Language
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.naicsoption import NAICSOption
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
from foundation_tenant.models.logevent import SortedLogEventByCreated
from foundation_tenant.models.commentpost import SortedCommentPostByCreated
from foundation_tenant.models.task import Task
from foundation_tenant.models.countryoption import CountryOption
from foundation_tenant.models.provinceoption import ProvinceOption
from foundation_tenant.models.cityoption import CityOption
from foundation_tenant.models.visitor import TenantVisitor
from foundation_tenant.models.inforesource import InfoResource


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

    @transaction.atomic
    def test_calendar_event_delete_all(self):
        # Setup our unit test.
        count = CalendarEvent.objects.all().count()
        self.assertEqual(count, 0)
        CalendarEvent.objects.bulk_create([
            CalendarEvent(id=1, owner=User.objects.get(username='1')),
            CalendarEvent(id=2, owner=User.objects.get(username='2')),
            CalendarEvent(id=3, owner=User.objects.get(username='3')),
            CalendarEvent(id=4, owner=User.objects.get(username='4')),
            CalendarEvent(id=5, owner=User.objects.get(username='5')),
        ])
        count = CalendarEvent.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        CalendarEvent.objects.delete_all()
        count = TenantMe.objects.all().count()
        self.assertEqual(count, 0)

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
    def test_ordered_log_event_delete_all(self):
        # Setup our unit test.
        count = SortedLogEventByCreated.objects.all().count()
        self.assertEqual(count, 0)
        SortedLogEventByCreated.objects.bulk_create([
            SortedLogEventByCreated(
                id = 1111,
                me=TenantMe.objects.create(
                    id = 1111,
                    owner=User.objects.get(username='1')
                ),
                text="Ice Age"
            ),
            SortedLogEventByCreated(
                id = 2222,
                me = TenantMe.objects.create(
                    id = 1112,
                    owner=User.objects.get(username='1'),
                ),
                text="Global Cooling"
            ),
            SortedLogEventByCreated(
                id = 3333,
                me = TenantMe.objects.create(
                    id = 1113,
                    owner=User.objects.get(username='1'),
                ),
                text="Solar Hibernation"
            ),
            SortedLogEventByCreated(
                id = 4444,
                me = TenantMe.objects.create(
                    id = 1114,
                    owner=User.objects.get(username='1'),
                ),
                text="Mini-Ice Age"
            ),
            SortedLogEventByCreated(
                id = 5555,
                me = TenantMe.objects.create(
                    id = 1115,
                    owner=User.objects.get(username='1'),
                ),
                text="Solar Reflective Particles"
            ),
        ])
        count = SortedLogEventByCreated.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        SortedLogEventByCreated.objects.delete_all()
        count = SortedLogEventByCreated.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        TenantMe.objects.delete_all()

    @transaction.atomic
    def test_ordered_log_event_delete_all(self):
        # Setup our unit test.
        count = SortedCommentPostByCreated.objects.all().count()
        self.assertEqual(count, 0)
        SortedCommentPostByCreated.objects.bulk_create([
            SortedCommentPostByCreated(
                id = 1111,
                me=TenantMe.objects.create(
                    id = 1111,
                    owner=User.objects.get(username='1')
                ),
                description="Ice Age"
            ),
            SortedCommentPostByCreated(
                id = 2222,
                me = TenantMe.objects.create(
                    id = 1112,
                    owner=User.objects.get(username='1'),
                ),
                description="Global Cooling"
            ),
            SortedCommentPostByCreated(
                id = 3333,
                me = TenantMe.objects.create(
                    id = 1113,
                    owner=User.objects.get(username='1'),
                ),
                description="Solar Hibernation"
            ),
            SortedCommentPostByCreated(
                id = 4444,
                me = TenantMe.objects.create(
                    id = 1114,
                    owner=User.objects.get(username='1'),
                ),
                description="Mini-Ice Age"
            ),
            SortedCommentPostByCreated(
                id = 5555,
                me = TenantMe.objects.create(
                    id = 1115,
                    owner=User.objects.get(username='1'),
                ),
                description="Solar Reflective Particles"
            ),
        ])
        count = SortedCommentPostByCreated.objects.all().count()
        self.assertEqual(count, 5)

        # Run our test and verify.
        SortedCommentPostByCreated.objects.delete_all()
        count = SortedLogEventByCreated.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        TenantMe.objects.delete_all()

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

    @transaction.atomic
    def test_governmentbenfitoption_delete_all(self):
        # Setup our unit test.
        count = GovernmentBenefitOption.objects.all().count()
        self.assertEqual(count, 0)
        GovernmentBenefitOption.objects.bulk_create([
            GovernmentBenefitOption(order_number=1, name='Transhumanism',),
            GovernmentBenefitOption(order_number=1, name='Space exploration',),
            GovernmentBenefitOption(order_number=1, name='Unlimited energy',),
            GovernmentBenefitOption(order_number=1, name='Defend hive',),
        ])
        count = GovernmentBenefitOption.objects.all().count()
        self.assertEqual(count, 4)

        # Run our test and verify.
        GovernmentBenefitOption.objects.delete_all()
        count = GovernmentBenefitOption.objects.all().count()
        self.assertEqual(count, 0)

    @transaction.atomic
    def test_identifyoption_delete_all(self):
        # Setup our unit test.
        count = IdentifyOption.objects.all().count()
        self.assertEqual(count, 0)
        IdentifyOption.objects.bulk_create([
            IdentifyOption(order_number=1, name='Transhumanism',),
            IdentifyOption(order_number=1, name='Space exploration',),
            IdentifyOption(order_number=1, name='Unlimited energy',),
            IdentifyOption(order_number=1, name='Defend hive',),
        ])
        count = IdentifyOption.objects.all().count()
        self.assertEqual(count, 4)

        # Run our test and verify.
        IdentifyOption.objects.delete_all()
        count = IdentifyOption.objects.all().count()
        self.assertEqual(count, 0)

    @transaction.atomic
    def test_countryoption_delete_all(self):
        # Setup our unit test.
        count = CountryOption.objects.all().count()
        self.assertEqual(count, 0)
        CountryOption.objects.bulk_create([
            CountryOption(name='Transhumanism',),
            CountryOption(name='Space exploration',),
            CountryOption(name='Unlimited energy',),
            CountryOption(name='Defend hive',),
        ])
        count = CountryOption.objects.all().count()
        self.assertEqual(count, 4)

        # Run our test and verify.
        CountryOption.objects.delete_all()
        count = CountryOption.objects.all().count()
        self.assertEqual(count, 0)

    @transaction.atomic
    def test_provinceoption_delete_all(self):
        # Setup our unit test.
        country = CountryOption.objects.create(
            name='hideauze.com',
        )
        count = ProvinceOption.objects.all().count()
        self.assertEqual(count, 0)
        ProvinceOption.objects.bulk_create([
            ProvinceOption(country=country, name='Transhumanism',),
            ProvinceOption(country=country, name='Space exploration',),
            ProvinceOption(country=country, name='Unlimited energy',),
            ProvinceOption(country=country, name='Defend hive',),
        ])
        count = ProvinceOption.objects.all().count()
        self.assertEqual(count, 4)

        # Run our test and verify.
        ProvinceOption.objects.delete_all()
        count = ProvinceOption.objects.all().count()
        self.assertEqual(count, 0)

    @transaction.atomic
    def test_cityoption_delete_all(self):
        # Setup our unit test.
        country = CountryOption.objects.create(
            name='hideauze.com',
        )
        province = ProvinceOption.objects.create(
            country=country,
            name='hideauze.com',
        )
        city = CityOption.objects.create(
            country=country,
            province=province,
            name='hideauze.com',
        )
        count = CityOption.objects.all().count()
        self.assertEqual(count, 0)
        CityOption.objects.bulk_create([
            CityOption(country=country, province=province, name='Transhumanism',),
            CityOption(country=country, province=province, name='Space exploration',),
            CityOption(country=country, province=province, name='Unlimited energy',),
            CityOption(country=country, province=province, name='Defend hive',),
        ])
        count = CityOption.objects.all().count()
        self.assertEqual(count, 4)

        # Run our test and verify.
        CityOption.objects.delete_all()
        count = CityOption.objects.all().count()
        self.assertEqual(count, 0)

        # Cleanup
        province.delete()
        country.delete()

    @transaction.atomic
    def test_countryoption_delete_all(self):
        # Setup our unit test.
        count = NAICSOption.objects.all().count()
        self.assertEqual(count, 0)
        NAICSOption.objects.bulk_create([
            NAICSOption(name='Transhumanism',),
            NAICSOption(name='Space exploration',),
            NAICSOption(name='Unlimited energy',),
            NAICSOption(name='Defend hive',),
        ])
        count = NAICSOption.objects.all().count()
        self.assertEqual(count, 4)

        # Run our test and verify.
        NAICSOption.objects.delete_all()
        count = NAICSOption.objects.all().count()
        self.assertEqual(count, 0)

    @transaction.atomic
    def test_countryoption_delete_all(self):
        # Setup our unit test.
        count = InfoResource.objects.all().count()
        self.assertEqual(count, 0)
        InfoResource.objects.bulk_create([
            InfoResource(name='Transhumanism',),
            InfoResource(name='Space exploration',),
            InfoResource(name='Unlimited energy',),
            InfoResource(name='Defend hive',),
        ])
        count = InfoResource.objects.all().count()
        self.assertEqual(count, 4)

        # Run our test and verify.
        InfoResource.objects.delete_all()
        count = InfoResource.objects.all().count()
        self.assertEqual(count, 0)
