from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_tenant.templatetags.foundation_tenant_tags import count_unread_messages
from foundation_tenant.templatetags.foundation_tenant_tags import count_new_intakes
from foundation_tenant.templatetags.foundation_tenant_tags import is_note_protected
from foundation_tenant.templatetags.foundation_tenant_tags import count_pending_tasks
from foundation_tenant.templatetags.foundation_tenant_tags import pretty_formatted_date
from foundation_tenant.models.base.message import Message
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.contactpoint import ContactPoint
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.task import Task
from foundation_tenant.models.base.note import Note
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRSTNAME = "Ledo"
TEST_USER_LASTNAME = ""


class FoundationTemplateTagsTestCase(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
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
        user = User.objects.create_user(  # Create our user.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English.
        super(FoundationTemplateTagsTestCase, self).setUp()

        # Initialize our test data.
        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)

    @transaction.atomic
    def tearDown(self):
        PostalAddress.objects.delete_all() # Must be first.
        ContactPoint.objects.delete_all()  # Must be second.
        Task.objects.delete_all()
        Intake.objects.delete_all()
        Note.objects.delete_all()
        Message.objects.delete_all()
        Me.objects.delete_all()
        items = User.objects.all()
        for item in items.all():
            item.delete()
        # super(FoundationTemplateTagsTestCase, self).tearDown()

    @transaction.atomic
    def test_count_unread_messages_with_one_result(self):
        # Create our sender.
        recipient, created = Me.objects.get_or_create(owner=self.user,)

        # Create our recipient
        sender_user = User.objects.create_user(
            email='chambers@gah.com',
            username='chambers',
            password='ILoveGAH'
        )
        sender_user.is_active = True
        sender_user.save()
        sender = Me.objects.create(
            id=666,
            owner=sender_user
        )

        # Create a new object with our specific test data.
        message = Message.objects.create(
            name="Unit Test",
            description="This is a unit test message.",
            recipient=recipient,
            sender=sender,
        )
        message.participants.add(sender, recipient)
        message.save()
        self.assertEqual(count_unread_messages(recipient.id), 1)

    @transaction.atomic
    def test_count_unread_messages_with_zero_results(self):
        # Create our sender.
        recipient, created = Me.objects.get_or_create(owner=self.user,)
        self.assertEqual(count_unread_messages(recipient.id), 0)

    @transaction.atomic
    def test_count_new_intakes_with_zero_results(self):
        self.assertEqual(count_new_intakes(), 0)

    @transaction.atomic
    def test_count_new_intakes_with_one_result(self):
        # Make Me setup.
        me = Me.objects.create(
            owner=self.user,
        )
        me.is_setup = True
        me.save()

        # Make Intake object.
        intake = Intake.objects.create(
            me=me,
            status=constants.PENDING_REVIEW_STATUS,
        )

        # Run test and verify.
        self.assertEqual(count_new_intakes(), 1)

    @transaction.atomic
    def test_is_note_protected_by_intake(self):
        # Create our data.
        me = Me.objects.create(
            owner=self.user,
        )
        note = Note.objects.create(
            name='Test',
            description='test',
            me=me,
        )
        Intake.objects.create(
            judgement_note=note,
            me=me,
            status=constants.PENDING_REVIEW_STATUS,
        )

        # Run our test and verify.
        self.assertTrue(is_note_protected(note))

    @transaction.atomic
    def test_is_note_protected_by_nothing(self):
        # Create our data.
        me = Me.objects.create(
            owner=self.user,
        )
        note = Note.objects.create(
            name='Test',
            description='test',
            me=me,
        )

        # Run our test and verify.
        self.assertFalse(is_note_protected(note))

    @transaction.atomic
    def test_count_pending_tasks(self):
        me = Me.objects.create(
            id=999,
            owner=self.user,
            notify_when_task_had_an_interaction=True,
        )
        task = Task.objects.create(
            id=666,
            owner=self.user,
            assigned_by=me,
            assignee=me,
            status=constants.OPEN_TASK_STATUS
        )
        task.participants.add(me)

        # Run our test and verify.
        self.assertEqual(count_pending_tasks(me), 1)

    @transaction.atomic
    def test_pretty_formatted_date(self):
        today = timezone.now()
        pretty_text = pretty_formatted_date(today)
        self.assertEqual(pretty_text, "Today")
