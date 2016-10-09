from django.core.signing import Signer
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_public.models.organization import PublicOrganization, PublicDomain
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.intake import Intake
from foundation_tenant.models.note import Note
from foundation_tenant.models.message import Message
from foundation_tenant.models.task import Task
from foundation_tenant.models.logevent import SortedLogEventByCreated
from foundation_tenant.models.commentpost import SortedCommentPostByCreated
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


# class FoundationEmailViewsWithPublicSchemaTestCases(APITestCase, TenantTestCase):
#     fixtures = []
#
#     def setup_tenant(self, tenant):
#         """Public Schema"""
#         tenant.schema_name = 'test'  # Do not change.
#         tenant.name = "Galactic Alliance of Humankind"
#         tenant.has_perks=True
#         tenant.has_mentors=True
#         tenant.how_discovered = "Command HQ"
#         tenant.how_many_served = 1
#
#     @classmethod
#     def setUpTestData(cls):
#         Group.objects.bulk_create([
#             Group(id=constants.ENTREPRENEUR_GROUP_ID, name="Entreprenuer",),
#             Group(id=constants.MENTOR_GROUP_ID, name="Mentor",),
#             Group(id=constants.ADVISOR_GROUP_ID, name="Advisor",),
#             Group(id=constants.ORGANIZATION_MANAGER_GROUP_ID, name="Org Manager",),
#             Group(id=constants.ORGANIZATION_ADMIN_GROUP_ID, name="Org Admin",),
#             Group(id=constants.CLIENT_MANAGER_GROUP_ID, name="Client Manager",),
#             Group(id=constants.SYSTEM_ADMIN_GROUP_ID, name="System Admin",),
#         ])
#         user = User.objects.create_user(  # Create our User.
#             email=TEST_USER_EMAIL,
#             username=TEST_USER_USERNAME,
#             password=TEST_USER_PASSWORD
#         )
#         user.is_active = True
#         user.save()
#
#     @transaction.atomic
#     def setUp(self):
#         translation.activate('en')  # Set English
#         super(FoundationEmailViewsWithPublicSchemaTestCases, self).setUp()
#
#         # Initialize our test data.
#         self.user = User.objects.get()
#         token = Token.objects.get(user__username=TEST_USER_USERNAME)
#
#         # Setup.
#         self.unauthorized_client = TenantClient(self.tenant)
#         self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)
#         self.authorized_client.login(
#             username=TEST_USER_USERNAME,
#             password=TEST_USER_PASSWORD
#         )
#
#     @transaction.atomic
#     def tearDown(self):
#         Intake.objects.delete_all()
#         Note.objects.delete_all()
#         PostalAddress.objects.delete_all()
#         ContactPoint.objects.delete_all()
#         TenantMe.objects.delete_all()
#         items = User.objects.all()
#         for item in items.all():
#             item.delete()
#         items = Group.objects.all()
#         for item in items.all():
#             item.delete()
#         # super(FoundationEmailViewsWithPublicSchemaTestCases, self).tearDown()
#
#     @transaction.atomic
#     def test_pass(self):
#         pass


class FoundationEmailViewsWithTenatSchemaTestCases(APITestCase, TenantTestCase):
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
        super(FoundationEmailViewsWithTenatSchemaTestCases, self).setUp()

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

        # Update Organization.
        self.tenant.users.add(self.user)
        self.tenant.save()

    @transaction.atomic
    def tearDown(self):
        SortedLogEventByCreated.objects.delete_all()
        SortedCommentPostByCreated.objects.delete_all()
        Task.objects.delete_all()
        Message.objects.delete_all()
        Intake.objects.delete_all()
        Note.objects.delete_all()
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        TenantMe.objects.delete_all()
        items = User.objects.all()
        for item in items.all():
            item.delete()
        items = Group.objects.all()
        for item in items.all():
            item.delete()
        # super(FoundationEmailViewsWithTenatSchemaTestCases, self).tearDown()

    @transaction.atomic
    def test_pending_intake_with_anonymous_user(self):
        url = reverse('foundation_email_pending_intake', args=[666,])
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, 'http://galacticalliance.example.com/en/login?next=/en/email/intake/pending/666/')

    @transaction.atomic
    def test_pending_intake_with_admin_user(self):
        target_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(target_group)
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        intake = Intake.objects.create(
            id=1,
            me=me,
            judgement_note=Note.objects.create(
                id=1,
                me=me,
                name="Space Citizen\'s Newsletter",
                description="Hail, citizen of the Galactic Alliance ...",
            )
        )
        url = reverse('foundation_email_pending_intake', args=[intake.id,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'A new Entrepreneur has completed the intake application.', response.content)

    @transaction.atomic
    def test_pending_intake_with_non_admin_user(self):
        target_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(target_group)
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        intake = Intake.objects.create(
            id=1,
            me=me,
            judgement_note=Note.objects.create(
                id=1,
                me=me,
                name="Space Citizen\'s Newsletter",
                description="Hail, citizen of the Galactic Alliance ...",
            )
        )
        url = reverse('foundation_email_pending_intake', args=[intake.id,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'403', response.content)

    @transaction.atomic
    def test_approved_intake_with_anonymous_user(self):
        url = reverse('foundation_email_approved_intake', args=[666,])
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, 'http://galacticalliance.example.com/en/login?next=/en/email/intake/approved/666/')

    @transaction.atomic
    def test_approved_intake_with_owner_user(self):
        target_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(target_group)
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        intake = Intake.objects.create(
            id=1,
            me=me,
            judgement_note=Note.objects.create(
                id=1,
                me=me,
                name="Space Citizen\'s Newsletter",
                description="Hail, citizen of the Galactic Alliance ...",
            )
        )
        url = reverse('foundation_email_approved_intake', args=[intake.id,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)

    @transaction.atomic
    def test_approved_intake_with_404(self):
        url = reverse('foundation_email_approved_intake', args=[666,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'404', response.content)

    @transaction.atomic
    def test_approved_intake_with_non_owner_user(self):
        target_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        user = User.objects.create_user(  # Create our User.
            email='h@g.com',
            username='1',
            password='1'
        )
        user.is_active = True
        user.save()
        user.groups.add(target_group)
        me = TenantMe.objects.create(
            id=666,
            owner=user,
        )
        intake = Intake.objects.create(
            id=666,
            me=me,
            judgement_note=Note.objects.create(
                id=666,
                me=me,
                name="Space Citizen\'s Newsletter",
                description="Hail, citizen of the Galactic Alliance ...",
            )
        )
        url = reverse('foundation_email_approved_intake', args=[intake.id,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'403', response.content)

    @transaction.atomic
    def test_rejected_intake_with_anonymous_user(self):
        url = reverse('foundation_email_rejected_intake', args=[666,])
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, 'http://galacticalliance.example.com/en/login?next=/en/email/intake/rejected/666/')

    @transaction.atomic
    def test_rejected_intake_with_owner_user(self):
        target_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(target_group)
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        intake = Intake.objects.create(
            id=1,
            me=me,
            judgement_note=Note.objects.create(
                id=1,
                me=me,
                name="Space Citizen\'s Newsletter",
                description="Hail, citizen of the Galactic Alliance ...",
            )
        )
        url = reverse('foundation_email_rejected_intake', args=[intake.id,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)

    @transaction.atomic
    def test_approved_intake_with_404(self):
        url = reverse('foundation_email_rejected_intake', args=[666,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'404', response.content)

    @transaction.atomic
    def test_approved_intake_with_non_owner_user(self):
        target_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        user = User.objects.create_user(  # Create our User.
            email='h@g.com',
            username='1',
            password='1'
        )
        user.is_active = True
        user.save()
        user.groups.add(target_group)
        me = TenantMe.objects.create(
            id=666,
            owner=user,
        )
        intake = Intake.objects.create(
            id=666,
            me=me,
            judgement_note=Note.objects.create(
                id=666,
                me=me,
                name="Space Citizen\'s Newsletter",
                description="Hail, citizen of the Galactic Alliance ...",
            )
        )
        url = reverse('foundation_email_rejected_intake', args=[intake.id,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'403', response.content)

    @transaction.atomic
    def test_message_with_anonymous_user(self):
        url = reverse('foundation_email_message', args=[666,])
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, 'http://galacticalliance.example.com/en/login?next=/en/email/message/666/')

    @transaction.atomic
    def test_message_with_404(self):
        url = reverse('foundation_email_message', args=[666,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'404', response.content)

    @transaction.atomic
    def test_message_with_participant(self):
        target_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(target_group)
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        message = Message.objects.create(
            sender=me,
            recipient=me,
            name="Space Citizen\'s Newsletter",
            description="Hail, citizen of the Galactic Alliance ...",
        )
        message.participants.add(me)
        url = reverse('foundation_email_message', args=[message.id,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Hail, citizen of the Galactic Alliance', response.content)

    @transaction.atomic
    def test_message_without_participant(self):
        target_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(target_group)
        me = TenantMe.objects.create(
            id=1,
            owner=self.user,
        )
        message = Message.objects.create(
            sender=me,
            recipient=me,
            name="Space Citizen\'s Newsletter",
            description="Hail, citizen of the Galactic Alliance ...",
        )
        url = reverse('foundation_email_message', args=[message.id,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'403', response.content)

    @transaction.atomic
    def test_tasks_with_anonymous_user(self):
        url = reverse('foundation_email_task', args=[666, 666,])
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, 'http://galacticalliance.example.com/en/login?next=/en/email/task/666/666/')

    @transaction.atomic
    def test_task_with_404(self):
        url = reverse('foundation_email_task', args=[666, 666,])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'404', response.content)

    @transaction.atomic
    def test_task_with_participant(self):
        target_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(target_group)
        me = TenantMe.objects.create(
            id=999,
            owner=self.user,
            notify_when_task_had_an_interaction=True,
        )
        log_event = SortedLogEventByCreated.objects.create(
            id=666,
            me=me,
            text="Hail, citizen of the Galactic Alliance ...",
        )
        task = Task.objects.create(
            id=666,
            owner=self.user,
            assigned_by=me,
            assignee=me,
            status=constants.OPEN_TASK_STATUS
        )
        task.participants.add(me)
        task.log_events.add(log_event)

        url = reverse('foundation_email_task', args=[task.id, log_event.id])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Hail, citizen of the Galactic Alliance', response.content)

    @transaction.atomic
    def test_task_without_participant(self):
        target_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.add(target_group)
        me = TenantMe.objects.create(
            id=999,
            owner=self.user,
            notify_when_task_had_an_interaction=True,
        )
        log_event = SortedLogEventByCreated.objects.create(
            id=666,
            me=me,
            text="Hail, citizen of the Galactic Alliance ...",
        )
        task = Task.objects.create(
            id=666,
            owner=self.user,
            assigned_by=me,
            assignee=me,
            status=constants.OPEN_TASK_STATUS
        )
        task.log_events.add(log_event)

        url = reverse('foundation_email_task', args=[task.id, log_event.id])
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'403', response.content)
