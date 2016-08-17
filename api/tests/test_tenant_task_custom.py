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
from api.views import authentication
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.task import Task
from foundation_tenant.models.orderedlogevent import OrderedLogEvent
from foundation_tenant.models.orderedcommentpost import OrderedCommentPost
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APITaskCustomWithTenantSchemaTestCase(APITestCase, TenantTestCase):
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
        super(APITaskCustomWithTenantSchemaTestCase, self).setUp()

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

        # Above taken from:
        # http://www.django-rest-framework.org/api-guide/testing/#authenticating

        # Initialize our test data.
        Task.objects.bulk_create([
            Task(owner=self.user),
            Task(owner=self.user),
            Task(owner=self.user),
        ])

    @transaction.atomic
    def tearDown(self):
        PostalAddress.objects.delete_all()  # Must be above Tasks.
        ContactPoint.objects.delete_all()   # Must be above Tasks.
        Task.objects.delete_all()
        OrderedLogEvent.objects.delete_all()
        OrderedCommentPost.objects.delete_all()
        TenantMe.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(APITaskCustomWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_log_event_with_anonymous_user(self):
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        task = Task.objects.create(
            id=666,
            assigned_by=me,
            assignee=me,
        )
        data = {
            'id': task.id,
            'text': 'Used for unit testing purposes.',
            'me': me.id,
        }
        response = self.unauthorized_client.put(
            '/api/tenanttask/666/log_event/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        log_event_count = OrderedLogEvent.objects.count()
        self.assertEqual(log_event_count, 0)
        self.assertEqual(len(mail.outbox), 0)

    @transaction.atomic
    def test_log_event_with_owner_user(self):
        me = TenantMe.objects.create(
            id=999,
            owner=self.user,
            notify_when_task_had_an_interaction=True,
        )
        task = Task.objects.create(
            id=666,
            owner=self.user,
            assigned_by=me,
            assignee=me,
        )
        task.participants.add(me)

        data = {
            'id': task.id,
            'text': 'Used for unit testing purposes.',
            'me': me.id,
        }
        response = self.authorized_client.put(
            '/api/tenanttask/666/log_event/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log_event_count = OrderedLogEvent.objects.count()
        self.assertEqual(log_event_count, 1)
        self.assertEqual(len(mail.outbox), 1)

    @transaction.atomic
    def test_log_event_with_different_owner_user(self):
        new_user = User.objects.create_user(  # Create our user.
            email='hideauze@evolvers.com',
            username='whalesquid',
            password='evolve_or_die'
        )
        new_user.is_active = True
        new_user.save()

        me = TenantMe.objects.create(
            id=666,
            owner=new_user,
            notify_when_task_had_an_interaction=True,
        )
        task = Task.objects.create(
            id=666,
            owner=new_user,
            assigned_by=me,
            assignee=me,
        )
        task.participants.add(me)

        data = {
            'id': task.id,
            'text': 'Used for unit testing purposes.',
            'me': me.id,
        }
        response = self.authorized_client.put(
            '/api/tenanttask/666/log_event/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log_event_count = OrderedLogEvent.objects.count()
        self.assertEqual(log_event_count, 1)
        self.assertEqual(len(mail.outbox), 1)

# post_comment
# complete_task
# incomplete_task
