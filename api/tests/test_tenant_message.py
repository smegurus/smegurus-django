import json
from django.db import transaction
from django.core import mail
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.http import QueryDict
from django.test import TestCase
from django.test import Client
from django.utils import translation
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_tenant.models.message import Message
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIMessageWithTenantSchemaTestCase(APITestCase, TenantTestCase):
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
        user.is_superuser = True
        user.is_active = True
        user.save()

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English.
        super(APIMessageWithTenantSchemaTestCase, self).setUp()

        # Initialize our test data.
        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)

        # Setup.
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)
        self.authorized_client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        self.tenant.owner = self.user
        self.tenant.save()

        # Above taken from:
        # http://www.django-rest-framework.org/api-guide/testing/#authenticating

    @transaction.atomic
    def tearDown(self):
        Message.objects.delete_all()
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        TenantMe.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(APIMessageWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_list_with_anonymous_user(self):
        response = self.unauthorized_client.get('/api/tenantmessage/?format=json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_authenticated_user(self):
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(org_admin_group)

        response = self.authorized_client.get('/api/tenantmessage/?format=json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_post_with_anonymous_user(self):
        data = {
            'name': 'Unit Test',
            'owner': self.user.id,
        }
        response = self.unauthorized_client.post(
            '/api/tenantmessage/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(mail.outbox), 0)

    @transaction.atomic
    def test_post_from_sender_to_recipient(self):
        # Create our recipient
        recipient_user = User.objects.create_user(  # Create our user.
            email='chambers@gah.com',
            username='chambers',
            password='ILoveGAH'
        )
        recipient_user.is_active = True
        recipient_user.save()
        recipient = TenantMe.objects.create(
            owner=recipient_user
        )

        # Run the test and verify.
        data = {
            'name': 'Unit Test',
            'recipient': recipient.id,
            'description': 'Glory to Galactic Alliance',
        }
        response = self.authorized_client.post(
            '/api/tenantmessage/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)

    @transaction.atomic
    def test_put_with_anonymous_user(self):
        # Create a new object with our specific test data.
        Message.objects.create(
            id=666,
            name="Unit Test",
            owner=self.user,
        )

        # Run the test.
        data = {
            'id': 666,
            'name': 'Unit Test',
            'owner': self.user.id,
        }
        response = self.unauthorized_client.put(
            '/api/tenantmessage/666/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(mail.outbox), 0)

    @transaction.atomic
    def test_put_with_original_sender(self):
        # Create our sender.
        sender = TenantMe.objects.create(
            owner=self.user,
        )

        # Create our recipient
        recipient_user = User.objects.create_user(  # Create our user.
            email='chambers@gah.com',
            username='chambers',
            password='ILoveGAH'
        )
        recipient_user.is_active = True
        recipient_user.save()
        recipient = TenantMe.objects.create(
            owner=recipient_user
        )

        # Create a new object with our specific test data.
        Message.objects.create(
            id=666,
            name="Unit Test #666",
            recipient=recipient,
            sender=sender,
        )

        # Run the test.
        data = {
            'id': 666,
            'name': 'Unit Test',
            'recipient': recipient.id,
        }
        response = self.authorized_client.put(
            '/api/tenantmessage/666/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0) # Editing does not qualify for email notification.


    @transaction.atomic
    def test_put_with_different_sender(self):
        # Create our CURRENT sender.
        TenantMe.objects.create(
            owner=self.user,
        )

        # Create our NEW sender.
        sender_user = User.objects.create_user(  # Create our user.
            email='whalesquid@hideauze.com',
            username='Whalesquid',
            password='ILoveHideauze'
        )
        sender_user.is_active = True
        sender_user.save()
        sender = TenantMe.objects.create(
            owner=sender_user
        )

        # Create our NEW recipient
        recipient_user = User.objects.create_user(  # Create our user.
            email='chambers@gah.com',
            username='chambers',
            password='ILoveGAH'
        )
        recipient_user.is_active = True
        recipient_user.save()
        recipient = TenantMe.objects.create(
            owner=recipient_user
        )

        # Create a new object with our specific test data.
        Message.objects.create(
            id=666,
            name="Unit Test #666",
            recipient=recipient,
            sender=sender,
        )

        # Run the test.
        data = {
            'id': 666,
            'name': 'Unit Test',
            'recipient': recipient.id,
        }
        response = self.authorized_client.put(
            '/api/tenantmessage/666/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(len(mail.outbox), 0)

    @transaction.atomic
    def test_delete_with_anonymous_user(self):
        # Create our CURRENT sender.
        sender = TenantMe.objects.create(
            owner=self.user,
        )

        # Create a new object with our specific test data.
        message = Message.objects.create(
            id=666,
            name="Unit Test #666",
            sender=sender,
        )
        message.participants.add(sender)
        message.save()

        # Run our test and verify.
        response = self.unauthorized_client.delete('/api/tenantmessage/666/?format=json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Message.objects.all().count(), 1)
        message = Message.objects.get(id=666)
        self.assertEqual(message.participants.count(), 1)

    @transaction.atomic
    def test_delete_with_sender(self):
        # Create our SENDER user.
        sender = TenantMe.objects.create(
            owner=self.user,
        )

        # Create our RECIPIENT user.
        recipient_user = User.objects.create_user(  # Create our user.
            email='chambers@gah.com',
            username='chambers',
            password='ILoveGAH'
        )
        recipient_user.is_active = True
        recipient_user.save()
        recipient = TenantMe.objects.create(
            owner=recipient_user
        )

        # Create a new object with our specific test data.
        message = Message.objects.create(
            id=666,
            name="Unit Test #666",
            sender=sender,
            recipient=recipient,
        )
        message.participants.add(sender)
        message.save()

        # Run our test and verify.
        response = self.authorized_client.delete('/api/tenantmessage/666/?format=json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Message.objects.all().count(), 1) # Check message has not been deleted
        message = Message.objects.get(id=666)
        self.assertEqual(message.participants.count(), 0)

    @transaction.atomic
    def test_delete_with_recipient(self):
        # Create our CURRENT sender.
        recipient = TenantMe.objects.create(
            owner=self.user,
        )

        # Create our NEW recipient
        sender_user = User.objects.create_user(  # Create our user.
            email='chambers@gah.com',
            username='chambers',
            password='ILoveGAH'
        )
        sender_user.is_active = True
        sender_user.save()
        sender = TenantMe.objects.create(
            owner=sender_user
        )

        # Create a new object with our specific test data.
        message = Message.objects.create(
            id=666,
            name="Unit Test #666",
            sender=sender,
            recipient=recipient,
        )
        message.participants.add(recipient, sender)
        message.save()

        # Run our test and verify.
        response = self.authorized_client.delete('/api/tenantmessage/666/?format=json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Message.objects.all().count(), 1) # Check message has not been deleted
        message = Message.objects.get(id=666)
        self.assertEqual(message.participants.count(), 1)

    @transaction.atomic
    def test_delete_with_different_sender(self):
        # Create our CURRENT sender.
        TenantMe.objects.create(
            owner=self.user,
        )

        # Create our NEW sender.
        sender_user = User.objects.create_user(  # Create our user.
            email='whalesquid@hideauze.com',
            username='Whalesquid',
            password='ILoveHideauze'
        )
        sender_user.is_active = True
        sender_user.save()
        sender = TenantMe.objects.create(
            owner=sender_user
        )

        # Create our NEW recipient
        recipient_user = User.objects.create_user(  # Create our user.
            email='chambers@gah.com',
            username='chambers',
            password='ILoveGAH'
        )
        recipient_user.is_active = True
        recipient_user.save()
        recipient = TenantMe.objects.create(
            owner=recipient_user
        )

        # Create a new object with our specific test data.
        message = Message.objects.create(
            id=666,
            name="Unit Test #666",
            recipient=recipient,
            sender=sender,
        )
        message.participants.add(recipient, sender)
        message.save()

        # Run our test and verify.
        response = self.authorized_client.delete('/api/tenantmessage/666/?format=json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Message.objects.all().count(), 1)
        message = Message.objects.get(id=666)
        self.assertEqual(message.participants.count(), 2)
