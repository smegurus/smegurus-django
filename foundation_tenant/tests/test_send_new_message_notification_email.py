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
from foundation_tenant.models.message import Message
from foundation_tenant.models.me import TenantMe
from foundation_public import constants
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
        users = User.objects.all()
        for user in users.all():
            user.delete()
        groups = Group.objects.all()
        for group in groups.all():
            group.delete()
        Message.objects.delete_all()
        TenantMe.objects.delete_all()
        # super(FoundationAuthSendNewMessageNotificationEmailWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_run_command_with_dne(self):
        call_command('send_new_message_notification_email', str(666))
        self.assertEqual(len(mail.outbox), 0)  # Test that one message has been sent.

    @transaction.atomic
    def test_run_command_with_success(self):
        sender = TenantMe.objects.create(  # Create our sender.
            owner=self.user,
        )

        recipient_user = User.objects.create_user(  # Create our recipient
            email='chambers@gah.com',
            username='chambers',
            password='ILoveGAH'
        )
        recipient_user.is_active = True
        recipient_user.save()
        recipient = TenantMe.objects.create(
            owner=recipient_user
        )

        Message.objects.create(  # Create a new object with our test data.
            id=666,
            name="Unit Test #666",
            recipient=recipient,
            sender=sender,
        )

        call_command('send_new_message_notification_email', str(666))  # Test
        self.assertEqual(len(mail.outbox), 1)  # Test that one message has been sent.
