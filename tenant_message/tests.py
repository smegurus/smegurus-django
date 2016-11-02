from django.db import transaction
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_tenant.models.message import Message
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.contactpoint import ContactPoint
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRST_NAME = "Ledo"
TEST_USER_LAST_NAME = ""


class TenantMessageTestCases(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galacticalliance'
        tenant.name = "Galactic Alliance of Humankind"
        tenant.is_setup = True
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
            User(email='6@6.com', username='6',password='6',is_active=True,),
            User(email='7@7.com', username='7',password='7',is_active=True,),
            User(email='8@8.com', username='8',password='8',is_active=True,),
            User(email='9@9.com', username='9',password='9',is_active=True,),
        ])
        user = User.objects.create_user(  # Create our User.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD,
            first_name=TEST_USER_FIRST_NAME,
            last_name=TEST_USER_LAST_NAME,
        )
        user.is_active = True
        user.save()

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English
        super(TenantMessageTestCases, self).setUp()
        # Initialize our test data.
        self.user = User.objects.get(username=TEST_USER_USERNAME)
        token = Token.objects.get(user=self.user)

        # Setup.
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)
        self.authorized_client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )

        # Update Organization.
        self.tenant.users.add(self.user)
        self.tenant.save()

    @transaction.atomic
    def tearDown(self):
        Message.objects.delete_all()
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        TenantMe.objects.delete_all()
        items = Group.objects.all()
        for item in items.all():
            item.delete()
        items = User.objects.all()
        for item in items.all():
            item.delete()
        # super(TenantMessageTestCases, self).tearDown()

    @transaction.atomic
    def test_inbox_page(self):
        url = reverse('tenant_message_inbox')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'id_table',response.content)

    @transaction.atomic
    def test_composer_page(self):
        url = reverse('tenant_message_composer')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'ajax_create_message',response.content)

    @transaction.atomic
    def test_specific_composer_page(self):
        recipient, created = TenantMe.objects.get_or_create(owner=self.user,)
        url = reverse('tenant_message_specific_composer', args=[recipient.id,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'ajax_create_message',response.content)

    @transaction.atomic
    def test_conversation_page(self):
        # Create our sender.
        recipient, created = TenantMe.objects.get_or_create(owner=self.user,)

        # Create our recipient
        sender_user = User.objects.create_user(
            email='chambers@gah.com',
            username='chambers',
            password='ILoveGAH'
        )
        sender_user.is_active = True
        sender_user.save()
        sender = TenantMe.objects.create(
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

        # Run the test and verify.
        url = reverse('tenant_conversation', args=[666,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'This is a unit test message.',response.content)

    @transaction.atomic
    def test_archive_conversation_page(self):
        # Create our sender.
        recipient = TenantMe.objects.create(
            id=999,
            owner=self.user,
        )

        # Create our recipient
        sender_user = User.objects.create_user(
            email='chambers@gah.com',
            username='chambers',
            password='ILoveGAH'
        )
        sender_user.is_active = True
        sender_user.save()
        sender = TenantMe.objects.create(
            id=666,
            owner=sender_user
        )

        # Create a new object with our specific test data.
        message = Message.objects.create(
            name="Unit Test #666",
            description="This is a test message.",
            recipient=recipient,
            sender=sender,
        )

        # Run the test and verify.
        url = reverse('tenant_archive_conversation', args=[666,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect happens.

    @transaction.atomic
    def test_archive_list_page(self):
        url = reverse('tenant_archive_inbox')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Archive',response.content)

    @transaction.atomic
    def test_archive_details_page(self):
        # Create our sender.
        recipient = TenantMe.objects.create(
            id=999,
            owner=self.user,
        )

        # Create our recipient
        sender_user = User.objects.create_user(
            email='chambers@gah.com',
            username='chambers',
            password='ILoveGAH'
        )
        sender_user.is_active = True
        sender_user.save()
        sender = TenantMe.objects.create(
            id=666,
            owner=sender_user
        )

        # Create a new object with our specific test data.
        message = Message.objects.create(
            name="Test Message",
            description="This is a test message.",
            recipient=recipient,
            sender=sender,
        )

        # Run the test and verify.
        url = reverse('tenant_archive_details', args=[666,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'This is a test message.',response.content)
