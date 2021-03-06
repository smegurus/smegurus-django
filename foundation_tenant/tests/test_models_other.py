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
from foundation_tenant.models.base.fileupload import FileUpload
from foundation_tenant.models.base.imageupload import ImageUpload
from foundation_tenant.models.base.governmentbenefitoption import GovernmentBenefitOption
from foundation_tenant.models.base.identifyoption import IdentifyOption
from foundation_tenant.models.base.language import Language
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.naicsoption import NAICSOption
from foundation_tenant.models.base.openinghoursspecification import OpeningHoursSpecification
from foundation_tenant.models.base.contactpoint import ContactPoint
from foundation_tenant.models.base.geocoordinate import GeoCoordinate
from foundation_tenant.models.base.abstract_place import AbstractPlace
from foundation_tenant.models.base.country import Country
from foundation_tenant.models.base.abstract_intangible import AbstractIntangible
from foundation_tenant.models.base.brand import Brand
from foundation_tenant.models.base.place import Place
from foundation_tenant.models.base.abstract_person import AbstractPerson
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.businessidea import BusinessIdea
from foundation_tenant.models.base.tellusyourneed import TellUsYourNeed
from foundation_tenant.models.base.calendarevent import CalendarEvent
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.admission import Admission
from foundation_tenant.models.base.faqitem import FAQItem
from foundation_tenant.models.base.faqgroup import FAQGroup
from foundation_tenant.models.base.communitypost import CommunityPost
from foundation_tenant.models.base.communityadvertisement import CommunityAdvertisement
from foundation_tenant.models.base.message import Message
from foundation_tenant.models.base.note import Note
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.logevent import SortedLogEventByCreated
from foundation_tenant.models.base.commentpost import SortedCommentPostByCreated
from foundation_tenant.models.base.task import Task
from foundation_tenant.models.base.countryoption import CountryOption
from foundation_tenant.models.base.provinceoption import ProvinceOption
from foundation_tenant.models.base.cityoption import CityOption
from foundation_tenant.models.base.visitor import Visitor


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
    def test_tenant_me_is_entrepreneur_with_false(self):
        # Attach non-entrepreneur group.
        group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        user = User.objects.get(username='1')
        user.groups.add(group)
        obj = Me.objects.create(
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
        obj = Me.objects.create(
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
        obj = Me.objects.create(
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
        obj = Me.objects.create(
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
        obj = Me.objects.create(
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
        obj = Me.objects.create(
            id=1,
            owner=user,
        )

        # Run the test and verify
        self.assertFalse(obj.is_manager())
        obj.delete()

    @transaction.atomic
    def test_tenant_get_by_owner_or_none_with_success(self):
        user = User.objects.get(username='1')
        Me.objects.create(
            id=999,
            owner=user,
        )
        me = Me.objects.get_by_owner_or_none(owner=user)
        self.assertIsNotNone(me)
        me.delete()

    @transaction.atomic
    def test_tenant_me_get_by_owner_or_none_with_none(self):
        target_me = Me.objects.create(
            id=666,
            owner=User.objects.get(username='1'),
        )
        search_me = Me.objects.get_by_owner_or_none(owner=User.objects.get(username='2'))
        self.assertIsNone(search_me)
        target_me.delete()

    @transaction.atomic
    def test_calendar_event_get_by_owner_or_none_with_none(self):
        target_me = Me.objects.create(
            id=666,
            owner=User.objects.get(username='1'),
        )
        search_me = Me.objects.get_by_owner_or_none(owner=User.objects.get(username='2'))
        self.assertIsNone(search_me)
        target_me.delete()

#TODO: IMPLEMENT
    # @transaction.atomic
    # def test_basic_task_get_absolute_url(self):
    #     me = Me.objects.create(
    #         id=1,
    #         owner=User.objects.get(username='1'),
    #         name='Ice Age',
    #     )
    #     obj = Task.objects.create(
    #         id=666,
    #         assigned_by=me,
    #         description="Ice Age"
    #     )
    #     self.assertIn(obj.get_absolute_url(), '/en/task/666/')
    #     obj.delete();  # Cleanup
    #     me.delete()
