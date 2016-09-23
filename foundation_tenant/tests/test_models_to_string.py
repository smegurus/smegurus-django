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
    def test_place_to_string(self):
        obj = Place.objects.create(
            name='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete();  # Cleanup

    @transaction.atomic
    def test_postaladdress_to_string(self):
        obj = PostalAddress.objects.create(
            name='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')

    @transaction.atomic
    def test_businessidea_to_string(self):
        obj = BusinessIdea.objects.create(
            name='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete()

    @transaction.atomic
    def test_tellusyourneed_to_string(self):
        obj = TellUsYourNeed.objects.create(
            id=2030,
            owner=User.objects.get(username='1')
        )
        self.assertIn(str(obj), '2030')
        obj.delete()

    @transaction.atomic
    def test_tag_to_string(self):
        obj = Tag.objects.create(
            name='Testing',
        )
        self.assertIn(str(obj), 'Testing')
        obj.delete()

    @transaction.atomic
    def test_openinghoursspecification_to_string(self):
        obj = OpeningHoursSpecification.objects.create(
            name='Testing',
        )
        self.assertIn(str(obj), 'Testing')
        obj.delete()

    @transaction.atomic
    def test_tenant_me_to_string(self):
        obj = TenantMe.objects.create(
            id=1,
            owner=User.objects.get(username='1'),
        )
        self.assertIn(str(obj), '1')
        obj.delete()

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
    def test_faqgroup_to_string(self):
        obj = FAQGroup.objects.create(
            text='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete();  # Cleanup

    @transaction.atomic
    def test_faqitem_to_string(self):
        obj = FAQItem.objects.create(
            question_text='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete();  # Cleanup

    @transaction.atomic
    def test_communitypost_to_string(self):
        obj = CommunityPost.objects.create(
            name='hideauze.com',
            owner=User.objects.get(username='1')
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete();  # Cleanup

    @transaction.atomic
    def test_communityadvertisement_to_string(self):
        obj = CommunityAdvertisement.objects.create(
            name='hideauze.com',
            owner=User.objects.get(username='1')
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete();  # Cleanup

    @transaction.atomic
    def test_message_to_string(self):
        obj = Message.objects.create(
            name='hideauze.com',
            owner=User.objects.get(username='1')
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete();  # Cleanup

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
    def test_ordered_log_event_to_string(self):
        me = TenantMe.objects.create(
            id=1,
            owner=User.objects.get(username='1'),
            name='Ice Age',
        )
        obj = SortedLogEventByCreated.objects.create(
            id=1,
            me=me,
            text="Ice Age"
        )
        self.assertIn(str(obj), 'Ice Age')
        obj.delete();  # Cleanup
        me.delete()

    @transaction.atomic
    def test_ordered_comment_post_to_string(self):
        me = TenantMe.objects.create(
            id=1,
            owner=User.objects.get(username='1'),
            name='Ice Age',
        )
        obj = SortedCommentPostByCreated.objects.create(
            id=1,
            me=me,
            description="Ice Age"
        )
        self.assertIn(str(obj), 'Ice Age')
        obj.delete();  # Cleanup
        me.delete()

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
    def test_governmentbenfitoption_to_string(self):
        obj = GovernmentBenefitOption.objects.create(
            order_number=1,
            name='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete()

    @transaction.atomic
    def test_identifyoption_to_string(self):
        obj = IdentifyOption.objects.create(
            order_number=1,
            name='hideauze.com',
        )
        self.assertIn(str(obj), 'hideauze.com')
        obj.delete()

    @transaction.atomic
    def test_countryoption_to_string(self):
        country = CountryOption.objects.create(
            name='hideauze.com',
        )
        self.assertIn(str(country), 'hideauze.com')
        country.delete()

    @transaction.atomic
    def test_provinceoption_to_string(self):
        country = CountryOption.objects.create(
            name='hideauze.com',
        )
        province = ProvinceOption.objects.create(
            country=country,
            name='hideauze.com',
        )
        self.assertIn(str(province), 'hideauze.com')
        province.delete()
        country.delete()

    @transaction.atomic
    def test_cityoption_to_string(self):
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
        self.assertIn(str(city), 'hideauze.com')
        city.delete()
        province.delete()
        country.delete()

    @transaction.atomic
    def test_naicsoption_to_string(self):
        option = NAICSOption.objects.create(
            name='hideauze.com',
        )
        self.assertIn(str(option), 'hideauze.com')
        option.delete()


    @transaction.atomic
    def test_info_resource_to_string(self):
        option = InfoResource.objects.create(
            name='hideauze.com',
        )
        self.assertIn(str(option), 'hideauze.com')
        option.delete()
