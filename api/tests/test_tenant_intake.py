import json
from django.core import mail
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
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_tenant.models.base.me import TenantMe
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.contactpoint import ContactPoint
from foundation_tenant.models.base.intake import Intake
from foundation_tenant.models.base.note import Note
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIIntakeWithTenantSchemaTestCase(APITestCase, TenantTestCase):
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
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        user = User.objects.create_user(  # Create our user.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        user.is_superuser = True
        user.is_active = True
        user.groups.add(org_admin_group)
        user.save()

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English.
        super(APIIntakeWithTenantSchemaTestCase, self).setUp()

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
        self.me = TenantMe.objects.create(
            owner=self.user,
        )

        # Above taken from:
        # http://www.django-rest-framework.org/api-guide/testing/#authenticating

    @transaction.atomic
    def tearDown(self):
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
        # super(APIIntakeWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_list_with_anonymous_user(self):
        response = self.unauthorized_client.get('/api/tenantintake/?format=json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_authenticated__user(self):
        # Change Group that the User belongs in.
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(entrepreneur_group)
        self.user.save()

        # Test and verify.
        response = self.authorized_client.get('/api/tenantintake/?format=json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_list_with_authenticated_management_group_user(self):
        # Change Group that the User belongs in.
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.remove(org_admin_group)
        self.user.save()

        # Test and verify.
        response = self.authorized_client.get('/api/tenantintake/?format=json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_list_with_authenticated_advisor_group_user(self):
        # Change Group that the User belongs in.
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.add(advisor_group)
        self.user.save()

        # Test and verify.
        response = self.authorized_client.get('/api/tenantintake/?format=json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_post_with_anonymous_user(self):
        data = {
            'me': self.me.id,
        }
        response = self.unauthorized_client.post('/api/tenantintake/?format=json', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_post_with_authenticated_management_group_user(self):
        # Run the test and verify.
        data = {
            'me': self.me.id,
        }
        response = self.authorized_client.post('/api/tenantintake/?format=json', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_post_with_authenticated_advisor_group_user(self):
        # Change Group that the User belongs in.
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.remove(org_admin_group)
        self.user.groups.add(advisor_group)
        self.user.save()

        # Test and verify.
        data = {
            'me': self.me.id,
        }
        response = self.authorized_client.post('/api/tenantintake/?format=json', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_put_with_anonymous_user(self):
        # Create a new object with our specific test data.
        Intake.objects.create(
            id=1,
            me=self.me,
        )

        # Run the test.
        data = {
            'id': 1,
            'me': self.me.id,
        }
        response = self.unauthorized_client.put('/api/tenantintake/1/?format=json', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_put_with_authenticated_management_user(self):
        # Create a new object with our specific test data.
        Intake.objects.create(
            id=1,
            me=self.me,
        )

        # Run the test.
        data = {
            'id': 1,
            'me': self.me.id,
        }
        response = self.authorized_client.put('/api/tenantintake/1/?format=json', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_put_with_authenticated_advisor_user(self):
        # Change Group that the User belongs in.
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.remove(org_admin_group)
        self.user.groups.add(advisor_group)
        self.user.save()

        # Create a new object with our specific test data.
        Intake.objects.create(
            id=1,
            me=self.me,
        )

        # Run the test.
        data = {
            'id': 1,
            'me': self.me.id,
        }
        response = self.authorized_client.put('/api/tenantintake/1/?format=json', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_delete_with_anonymous_user(self):
        Intake.objects.create(
            id=1,
            me=self.me,
        )
        response = self.unauthorized_client.delete('/api/tenantintake/1/?format=json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_with_authenticated_management_user(self):
        Intake.objects.create(
            id=1,
            me=self.me,
            judgement_note=Note.objects.create(
                id=1,
                me=self.me,
            ),
            privacy_note=Note.objects.create(
                id=2,
                me=self.me,
            ),
            terms_note=Note.objects.create(
                id=3,
                me=self.me,
            ),
            confidentiality_note=Note.objects.create(
                id=4,
                me=self.me,
            ),
            collection_note=Note.objects.create(
                id=5,
                me=self.me,
            ),
        )
        response = self.authorized_client.delete('/api/tenantintake/1/?format=json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def test_delete_with_authenticated_advisor_user(self):
        # Create our object to be deleted.

        Intake.objects.create(
            id=1,
            me=self.me,
            status=constants.CREATED_STATUS,
            judgement_note=Note.objects.create(
                id=1,
                me=self.me,
            ),
        )

        # Change Group that the User belongs in.
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        advisor_group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.remove(org_admin_group)
        self.user.groups.add(advisor_group)
        self.user.save()

        # Run test and verify.
        response = self.authorized_client.delete('/api/tenantintake/1/?format=json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def test_complete_intake_with_anonymous_user(self):
        # Setup our object.
        Intake.objects.create(
            id=1,
            me=self.me,
            status=constants.PENDING_REVIEW_STATUS,
            judgement_note=Note.objects.create(
                id=1,
                me=self.me,
            ),
        )

        # Run the test and verify.
        response = self.unauthorized_client.put(
            '/api/tenantintake/1/complete_intake/?format=json',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        me = Intake.objects.get(id=1)
        self.assertEqual(me.status, constants.PENDING_REVIEW_STATUS)
        self.assertEqual(len(mail.outbox), 0)  # Test that one message has not been sent.

    @transaction.atomic
    def test_complete_intake_with_owner_user(self):
        # Setup our object.
        Intake.objects.create(
            id=1,
            me=self.me,
            status=constants.CREATED_STATUS,
        )

        # Run the test and verify.
        response = self.authorized_client.put(
            '/api/tenantintake/1/complete_intake/?format=json',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        me = Intake.objects.get(id=1)
        self.assertEqual(me.status, constants.PENDING_REVIEW_STATUS)

        # Test that one email has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'New Entrepreneur Application!')

    @transaction.atomic
    def test_complete_intake_with_different_owner_user(self):
        # Setup our objects.
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        new_user = User.objects.create_user(  # Create our user.
            email='chambers@gah.com',
            username='Chambers',
            password='I do not like Stryker',
        )
        new_user.is_active = True
        new_user.groups.add(org_admin_group)
        new_user.save()
        new_me = TenantMe.objects.create(
            owner=new_user
        )
        Intake.objects.create(
            id=1,
            me=new_me,
            status=constants.CREATED_STATUS,
        )

        # Run the test and verify.
        response = self.authorized_client.put(
            '/api/tenantintake/1/complete_intake/?format=json',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        me = Intake.objects.get(id=1)
        self.assertEqual(me.status, constants.CREATED_STATUS)
        self.assertEqual(len(mail.outbox), 0)  # Test that one message has not been sent.

    @transaction.atomic
    def test_complete_intake_with_owner_user_with_404(self):
        # Setup our object.
        Intake.objects.create(
            id=1,
            me=self.me,
            status=constants.CREATED_STATUS,
        )

        # Run the test and verify.
        response = self.authorized_client.put(
            '/api/tenantintake/6666/complete_intake/?format=json',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        me = Intake.objects.get(id=1)
        self.assertEqual(me.status, constants.CREATED_STATUS)
        self.assertEqual(len(mail.outbox), 0)  # Test that one message has not been sent.

    @transaction.atomic
    def test_judge_with_anonymous_user(self):
        # Create a new object with our specific test data.
        # Setup our object.
        Intake.objects.create(
            id=1,
            me=self.me,
            status=constants.CREATED_STATUS,
        )

        # Run the test.
        data = {
            'id': 1,
            'owner': self.user.id,
            'is_employee_created': False,
        }
        response = self.unauthorized_client.put(
            '/api/tenantintake/1/judge/?format=json',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        intake = Intake.objects.get(id=1)
        self.assertEqual(intake.status, constants.CREATED_STATUS)
        self.assertFalse(intake.me.is_admitted)
        self.assertEqual(len(mail.outbox), 0)  # Test that one message has not been sent.

    @transaction.atomic
    def test_judge_with_employee_user_for_existing_intake_with_note(self):
        # Setup our object.
        Intake.objects.create(
            id=1,
            me=self.me,
            status=constants.CREATED_STATUS,
            judgement_note=Note.objects.create(
                me=self.me,
            ),
        )

        # Run the test and verify.
        response = self.authorized_client.put(
            '/api/tenantintake/1/judge/?format=json',
            json.dumps({
                'status': constants.APPROVED_STATUS,
                'comment': 'This is a test comment.',
                'is_employee_created': False,
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        intake = Intake.objects.get(id=1)
        self.assertEqual(intake.status, constants.APPROVED_STATUS)
        self.assertTrue(intake.me.is_admitted)
        note = Note.objects.get(id=1)
        self.assertIn('This is a test comment.', note.description)
        self.assertEqual(len(mail.outbox), 1)  # Test that one message has been sent.
        self.assertIn('Accepted', mail.outbox[0].subject)

    @transaction.atomic
    def test_judge_with_employee_user_for_existing_intake_without_note(self):
        # Setup our object.
        Intake.objects.create(
            id=1,
            me=self.me,
            status=constants.CREATED_STATUS,
        )

        # Run the test and verify.
        response = self.authorized_client.put(
            '/api/tenantintake/1/judge/?format=json',
            json.dumps({
                'status': constants.REJECTED_STATUS,
                'comment': 'This is a test comment.',
                'is_employee_created': False,
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        intake = Intake.objects.get(id=1)
        self.assertEqual(intake.status, constants.REJECTED_STATUS)
        self.assertFalse(intake.me.is_admitted)
        note = Note.objects.get(id=1)
        self.assertIn('This is a test comment.', note.description)
        self.assertEqual(len(mail.outbox), 1)  # Test that one message has been sent.
        self.assertIn('Rejected', mail.outbox[0].subject)

    @transaction.atomic
    def test_judge_with_employee_user_for_manually_created_intake(self):
        # Setup our object.
        Intake.objects.create(
            id=1,
            me=self.me,
            status=constants.CREATED_STATUS,
        )

        # Run the test and verify.
        response = self.authorized_client.put(
            '/api/tenantintake/1/judge/?format=json',
            json.dumps({
                'status': constants.APPROVED_STATUS,
                'comment': 'This is a test comment.',
                'is_employee_created': True,
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        intake = Intake.objects.get(id=1)
        self.assertEqual(intake.status, constants.APPROVED_STATUS)
        self.assertTrue(intake.me.is_admitted)
        note = Note.objects.get(id=1)
        self.assertIn('This is a test comment.', note.description)
        self.assertEqual(len(mail.outbox), 1)  # Test that one message has been sent.

    @transaction.atomic
    def test_judge_with_non_employee_user(self):
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.remove(org_admin_group)
        group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(group)
        Intake.objects.create(
            id=1,
            me=self.me,
            status=constants.CREATED_STATUS,
        )

        # Run the test.
        response = self.authorized_client.put(
            '/api/tenantintake/1/judge/?format=json',
            json.dumps({
                'status': constants.APPROVED_STATUS,
                'comment': 'This is a test comment.',
                'is_employee_created': False,
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        intake = Intake.objects.get(id=1)
        self.assertEqual(intake.status, constants.CREATED_STATUS)
        self.assertFalse(intake.me.is_admitted)
        self.assertEqual(len(mail.outbox), 0)  # Test that one message has not been sent.

    @transaction.atomic
    def test_judge_with_owner_user_with_404(self):
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        self.user.groups.remove(org_admin_group)
        group = Group.objects.get(id=constants.ADVISOR_GROUP_ID)
        self.user.groups.add(group)

        response = self.authorized_client.put(
            '/api/tenantintake/666/judge/?format=json',
            json.dumps({
                'status': constants.APPROVED_STATUS,
                'comment': 'This is a test comment.',
                'is_employee_created': False,
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(b'No Intake matches the given query.', response.content)
        self.assertEqual(len(mail.outbox), 0)  # Test that one message has not been sent.

    @transaction.atomic
    def test_crm_update_with_anonymous_user(self):
        # Setup our object.
        Intake.objects.create(
            id=1,
            me=self.me,
            status=constants.PENDING_REVIEW_STATUS,
            has_signed_with_name="Ledo"
        )

        # Run the test and verify.
        response = self.unauthorized_client.put(
            '/api/tenantintake/1/crm_update/?format=json',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_crm_update_with_owner_user(self):
        # Setup our object.
        Intake.objects.create(
            id=1,
            me=self.me,
            status=constants.CREATED_STATUS,
            has_signed_with_name="Ledo"
        )

        # Run the test and verify.
        response = self.authorized_client.put(
            '/api/tenantintake/1/crm_update/?format=json',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_crm_update_with_different_owner_user(self):
        # Setup our objects.
        org_admin_group = Group.objects.get(id=constants.ORGANIZATION_ADMIN_GROUP_ID)
        new_user = User.objects.create_user(  # Create our user.
            email='chambers@gah.com',
            username='Chambers',
            password='I do not like Stryker',
        )
        new_user.is_active = True
        new_user.groups.add(org_admin_group)
        new_user.save()
        new_me = TenantMe.objects.create(
            owner=new_user
        )
        Intake.objects.create(
            id=1,
            me=new_me,
            status=constants.CREATED_STATUS,
            has_signed_with_name="Ledo"
        )

        # Run the test and verify.
        response = self.authorized_client.put(
            '/api/tenantintake/1/crm_update/?format=json',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_crm_update_with_owner_user_with_404(self):
        # Run the test and verify.
        response = self.authorized_client.put(
            '/api/tenantintake/6666/crm_update/?format=json',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
