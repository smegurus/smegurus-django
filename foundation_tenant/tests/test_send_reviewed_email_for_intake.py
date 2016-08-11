from django.core import mail
from django.core.urlresolvers import resolve, reverse
from django.core.management import call_command
from django.db import transaction
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.intake import Intake
from smegurus import constants
from smegurus.settings import env_var


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class FoundationAuthSendNewMessageNotificationEmailWithPublicSchemaTestCase(APITestCase, TenantTestCase):
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
        user = User.objects.create_user(  # Create our User.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English
        super(FoundationAuthSendNewMessageNotificationEmailWithPublicSchemaTestCase, self).setUp()
        self.user = User.objects.get()

    @transaction.atomic
    def tearDown(self):
        Intake.objects.delete_all()
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        TenantMe.objects.delete_all()
        items = User.objects.all()
        for item in items.all():
            item.delete()
        items = Group.objects.all()
        for item in items.all():
            item.delete()
        # super(FoundationAuthSendNewMessageNotificationEmailWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_run_command_with_dne(self):
        call_command('send_reviewed_email_for_intake', str(666))
        self.assertEqual(len(mail.outbox), 0)  # Test that one message has been sent.

    @transaction.atomic
    def test_run_command_for_case_1(self):
        me = TenantMe.objects.create(  # Create our sender.
            owner=self.user,
        )

        intake = Intake.objects.create(
            me=me,
            is_employee_created=True,
            status=constants.APPROVED_STATUS,
        )

        call_command('send_reviewed_email_for_intake', str(intake.id))  # Test
        self.assertEqual(len(mail.outbox), 1)  # Test that one message has been sent.

    @transaction.atomic
    def test_run_command_for_case_2(self):
        me = TenantMe.objects.create(  # Create our sender.
            owner=self.user,
        )

        intake = Intake.objects.create(
            me=me,
            is_employee_created=False,
            status=constants.APPROVED_STATUS,
        )

        call_command('send_reviewed_email_for_intake', str(intake.id))  # Test
        self.assertEqual(len(mail.outbox), 1)  # Test that one message has been sent.

    @transaction.atomic
    def test_run_command_for_case_3(self):
        me = TenantMe.objects.create(  # Create our sender.
            owner=self.user,
        )

        intake = Intake.objects.create(
            me=me,
            is_employee_created=False,
            status=constants.REJECTED_STATUS,
        )

        call_command('send_reviewed_email_for_intake', str(intake.id))  # Test
        self.assertEqual(len(mail.outbox), 1)  # Test that one message has been sent.
