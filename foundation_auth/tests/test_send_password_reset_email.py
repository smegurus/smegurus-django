from django.core import mail
from django.core.urlresolvers import resolve, reverse
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
from tenant_schemas.test.cases import TenantTestCase
from tenant_schemas.test.client import TenantClient
from django.core.management import call_command
from smegurus import constants
from smegurus.settings import env_var


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class FoundationAuthSendPasswordResetEmailWithPublicSchemaTestCase(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Public Schema"""
        tenant.schema_name = 'test'  # Do not change this!
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
        super(FoundationAuthSendPasswordResetEmailWithPublicSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)
        self.user = User.objects.get()

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        groups = Group.objects.all()
        for group in groups.all():
            group.delete()
        super(FoundationAuthSendPasswordResetEmailWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_send_password_reset_email(self):
        # Attach User to group.
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(org_admin_group)
        self.user.save()

        # Test
        call_command('send_password_reset_email',str(TEST_USER_EMAIL))

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

    @transaction.atomic
    def test_api_send_activation_with_no_email(self):
        call_command('send_password_reset_email',str('blah@blah.com'))

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 0)
