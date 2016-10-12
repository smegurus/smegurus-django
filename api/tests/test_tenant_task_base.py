import json
from django.db import transaction
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
from tenant_schemas.test.cases import TenantTestCase
from tenant_schemas.test.client import TenantClient
from api.views import authentication
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.task import Task
from foundation_tenant.models.logevent import SortedLogEventByCreated
from foundation_tenant.models.commentpost import SortedCommentPostByCreated
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.calendarevent import CalendarEvent
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APITaskBaseWithTenantSchemaTestCase(APITestCase, TenantTestCase):
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
        super(APITaskBaseWithTenantSchemaTestCase, self).setUp()

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
        CalendarEvent.objects.delete_all()
        Task.objects.delete_all()
        SortedLogEventByCreated.objects.delete_all()
        SortedCommentPostByCreated.objects.delete_all()
        TenantMe.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(APITaskBaseWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_list_with_anonymous_user(self):
        response = self.unauthorized_client.get('/api/tenanttask/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_authenticated_user(self):
        me = TenantMe.objects.create(  # Create our models.
            id=1,
            owner=self.user,
        )
        task = Task.objects.create(
            id=666,
            assigned_by=me,
            assignee=me,
        )
        response = self.authorized_client.get('/api/tenanttask/')  # Run test and verify.
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_post_with_anonymous_user(self):
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'assigned_by': me.id,
            'assignee': me.id,
            'status': constants.OPEN_TASK_STATUS,
        }
        response = self.unauthorized_client.post(
            '/api/tenanttask/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_post_with_authenticated_user(self):
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'assigned_by': me.id,
            'assignee': me.id,
            'status': constants.OPEN_TASK_STATUS,
        }
        response = self.authorized_client.post(
            '/api/tenanttask/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_put_with_anonymous_user(self):
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
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'assigned_by': me.id,
            'assignee': me.id,
            'status': constants.OPEN_TASK_STATUS,
        }
        response = self.unauthorized_client.put(
            '/api/tenanttask/666/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_put_with_owner_user(self):
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        task = Task.objects.create(
            id=666,
            owner=self.user,
            assigned_by=me,
            assignee=me,
        )
        data = {
            'id': task.id,
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'assigned_by': me.id,
            'assignee': me.id,
            'status': constants.OPEN_TASK_STATUS,
        }
        response = self.authorized_client.put(
            '/api/tenanttask/666/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_delete_by_anonymous_user(self):
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        task = Task.objects.create(
            id=666,
            owner=self.user,
            assigned_by=me,
            assignee=me,
        )
        response = self.unauthorized_client.delete('/api/tenanttask/'+str(task.id)+'/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_by_owner_user(self):
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        calendar_event = CalendarEvent.objects.create(
            id=666,
            owner=self.user
        )
        task = Task.objects.create(
            id=666,
            owner=self.user,
            assigned_by=me,
            assignee=me,
            calendar_event=calendar_event
        )
        response = self.authorized_client.delete('/api/tenanttask/'+str(task.id)+'/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
