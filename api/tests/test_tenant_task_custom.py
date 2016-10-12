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
        CalendarEvent.objects.delete_all()
        Task.objects.delete_all()
        SortedLogEventByCreated.objects.delete_all()
        SortedCommentPostByCreated.objects.delete_all()
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
            status=constants.OPEN_TASK_STATUS
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
        log_event_count = SortedLogEventByCreated.objects.count()
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
            status=constants.OPEN_TASK_STATUS
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
        log_event_count = SortedLogEventByCreated.objects.count()
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
            status=constants.OPEN_TASK_STATUS
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
        log_event_count = SortedLogEventByCreated.objects.count()
        self.assertEqual(log_event_count, 1)
        self.assertEqual(len(mail.outbox), 1)

    @transaction.atomic
    def test_post_comment_with_anonymous_user(self):
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        task = Task.objects.create(
            id=666,
            assigned_by=me,
            assignee=me,
            status=constants.OPEN_TASK_STATUS
        )
        data = {
            'id': task.id,
            'text': 'Used for unit testing purposes.',
            'me': me.id,
        }
        response = self.unauthorized_client.put(
            '/api/tenanttask/666/post_comment/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        count = SortedCommentPostByCreated.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(len(mail.outbox), 0)
        log_event_count = SortedLogEventByCreated.objects.count()
        self.assertEqual(log_event_count, 0)

    @transaction.atomic
    def test_post_comment_with_owner_user(self):
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
            status=constants.OPEN_TASK_STATUS
        )
        task.participants.add(me)

        data = {
            'id': task.id,
            'text': 'Used for unit testing purposes.',
            'me': me.id,
        }
        response = self.authorized_client.put(
            '/api/tenanttask/666/post_comment/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count = SortedCommentPostByCreated.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(len(mail.outbox), 1)
        log_event_count = SortedLogEventByCreated.objects.count()
        self.assertEqual(log_event_count, 1)

    @transaction.atomic
    def test_post_comment_with_different_owner_user(self):
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
            status=constants.OPEN_TASK_STATUS
        )
        task.participants.add(me)

        data = {
            'id': task.id,
            'text': 'Used for unit testing purposes.',
            'me': me.id,
        }
        response = self.authorized_client.put(
            '/api/tenanttask/666/post_comment/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count = SortedCommentPostByCreated.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(len(mail.outbox), 1)
        log_event_count = SortedLogEventByCreated.objects.count()
        self.assertEqual(log_event_count, 1)


    @transaction.atomic
    def test_complete_task_with_anonymous_user(self):
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        task = Task.objects.create(
            id=666,
            assigned_by=me,
            assignee=me,
            status=constants.OPEN_TASK_STATUS
        )
        data = {
            'id': task.id,
            'text': 'Used for unit testing purposes.',
            'me': me.id,
        }
        response = self.unauthorized_client.put(
            '/api/tenanttask/666/complete_task/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        count = SortedCommentPostByCreated.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(len(mail.outbox), 0)
        log_event_count = SortedLogEventByCreated.objects.count()
        self.assertEqual(log_event_count, 0)
        task = Task.objects.get(pk=666)
        self.assertEqual(task.status, constants.OPEN_TASK_STATUS)

    @transaction.atomic
    def test_complete_task_with_owner_user(self):
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
            status=constants.OPEN_TASK_STATUS,
        )
        task.participants.add(me)

        data = {
            'id': task.id,
            'text': 'Used for unit testing purposes.',
            'me': me.id,
        }
        response = self.authorized_client.put(
            '/api/tenanttask/666/complete_task/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        log_event_count = SortedLogEventByCreated.objects.count()
        self.assertEqual(log_event_count, 1)
        task = Task.objects.get(pk=666)
        self.assertEqual(task.status, constants.CLOSED_TASK_STATUS)

    @transaction.atomic
    def test_complete_task_with_different_owner_user(self):
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
            status=constants.OPEN_TASK_STATUS
        )
        task.participants.add(me)

        data = {
            'id': task.id,
            'text': 'Used for unit testing purposes.',
            'me': me.id,
        }
        response = self.authorized_client.put(
            '/api/tenanttask/666/complete_task/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        log_event_count = SortedLogEventByCreated.objects.count()
        self.assertEqual(log_event_count, 1)
        task = Task.objects.get(pk=666)
        self.assertEqual(task.status, constants.CLOSED_TASK_STATUS)

    @transaction.atomic
    def test_incomplete_task_with_anonymous_user(self):
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        task = Task.objects.create(
            id=666,
            assigned_by=me,
            assignee=me,
            status=constants.OPEN_TASK_STATUS,
        )
        data = {
            'id': task.id,
            'text': 'Used for unit testing purposes.',
            'me': me.id,
        }
        response = self.unauthorized_client.put(
            '/api/tenanttask/666/incomplete_task/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        count = SortedCommentPostByCreated.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(len(mail.outbox), 0)
        log_event_count = SortedLogEventByCreated.objects.count()
        self.assertEqual(log_event_count, 0)
        task = Task.objects.get(pk=666)
        self.assertEqual(task.status, constants.OPEN_TASK_STATUS)

    @transaction.atomic
    def test_incomplete_task_with_owner_user(self):
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
            status=constants.OPEN_TASK_STATUS,
        )
        task.participants.add(me)

        data = {
            'id': task.id,
            'text': 'Used for unit testing purposes.',
            'me': me.id,
        }
        response = self.authorized_client.put(
            '/api/tenanttask/666/incomplete_task/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        log_event_count = SortedLogEventByCreated.objects.count()
        self.assertEqual(log_event_count, 1)
        task = Task.objects.get(pk=666)
        self.assertEqual(task.status, constants.INCOMPLETE_TASK_STATUS)

    @transaction.atomic
    def test_incomplete_task_with_different_owner_user(self):
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
            status=constants.OPEN_TASK_STATUS,
        )
        task.participants.add(me)

        data = {
            'id': task.id,
            'text': 'Used for unit testing purposes.',
            'me': me.id,
        }
        response = self.authorized_client.put(
            '/api/tenanttask/666/incomplete_task/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)
        log_event_count = SortedLogEventByCreated.objects.count()
        self.assertEqual(log_event_count, 1)
        task = Task.objects.get(pk=666)
        self.assertEqual(task.status, constants.INCOMPLETE_TASK_STATUS)

    @transaction.atomic
    def test_set_calendar_event_with_anonymous_user(self):
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        task = Task.objects.create(
            id=666,
            assigned_by=me,
            assignee=me,
            status=constants.OPEN_TASK_STATUS,
        )
        data = {
            'datetime': '2016-09-20 18:16:36.687365-04',
        }
        response = self.unauthorized_client.put(
            '/api/tenanttask/666/set_calendar_event/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_set_calendar_event_with_owner_user(self):
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
            status=constants.OPEN_TASK_STATUS,
        )
        task.participants.add(me)

        #--------------------#
        # CASE 1 OF 4: VALID #
        #--------------------#
        data = {
            'datetime': '2016-09-20 18:16:36.687365-04',
        }
        response = self.authorized_client.put(
            '/api/tenanttask/666/set_calendar_event/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #------------------------#
        # CASE 2 OF 4: NOT VALID #
        #------------------------#
        data = {
            'datetime': 'da future yo',
        }
        response = self.authorized_client.put(
            '/api/tenanttask/666/set_calendar_event/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #-------------------------------#
        # CASE 3 OF 4: MISSING ASSIGNEE #
        #-------------------------------#
        task.assignee = None
        task.save()
        data = {
            'datetime': '2016-09-20 18:16:36.687365-04',
        }
        response = self.authorized_client.put(
            '/api/tenanttask/666/set_calendar_event/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #--------------------------------#
        # CASE 4 OF 4: VALID WITH DELETE #
        #--------------------------------#
        task.assignee = me
        task.save()
        data = {
            'datetime': '2016-09-20 18:16:36.687365-04',
        }
        response = self.authorized_client.put(
            '/api/tenanttask/666/set_calendar_event/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
