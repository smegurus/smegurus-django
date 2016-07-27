from django.db import transaction
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_public import constants
from foundation_tenant.models.me import TenantMe
from tenant_profile.decorators import tenant_profile_required


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRST_NAME = "Ledo"
TEST_USER_LAST_NAME = ""


class TenantProfileTestCases(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galacticalliance'
        tenant.name = "Galactic Alliance of Humankind"
        tenant.is_setup = True

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
        super(TenantProfileTestCases, self).setUp()
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

        # Setup User.
        TenantMe.objects.create(
            owner=self.user,
        )

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        items = Token.objects.all()
        for item in items.all():
            item.delete()
        # super(TenantProfileTestCases, self).tearDown()

    @transaction.atomic
    def test_profile_page(self):
        url = reverse('tenant_profile')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Profile',response.content)

    @transaction.atomic
    def test_profile_settings_page(self):
        url = reverse('tenant_profile_setting')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'Personal Settings',response.content)

#    @transaction.atomic
#    def test_locked_page(self):
#        """Load up the lock page and verify User is locked afterwards"""
#        # Pre-test to verify the User is NOT locked out.
#        me = PublicMe.objects.get(owner=self.user)
#        self.assertFalse(me.is_locked)
#
#        # Run our test.
#        url = reverse('tenant_profile_lock')
#        response = self.authorized_client.get(url)
#        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        self.assertTrue(len(response.content) > 1)
#        # self.assertIn(b'Profile Settings',response.content)
#
#        # Verfiy our User has been locked out.
#        me = PublicMe.objects.get(owner=self.user)
#        self.assertTrue(me.is_locked)
#
#    @transaction.atomic
#    def test_tenant_profile_required_decorator_with_redirect(self):
#        """Load up the lock page and verify User is locked afterwards"""
#        # Pre-configure to lock the user out.
#        me = PublicMe.objects.get(owner=self.user)
#        me.is_locked = True
#        me.save()
#
#        # Run our test.
#        url = reverse('tenant_profile_is_locked')
#        response = self.authorized_client.get(url)
#        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
#        self.assertRedirects(response, reverse('tenant_profile_lock'))
#
#    @transaction.atomic
#    def test_tenant_profile_required_decorator_without_redirect(self):
#        """Load up the lock page and verify User is locked afterwards"""
#        # Run our test.
#        url = reverse('tenant_profile_is_locked')
#        response = self.authorized_client.get(url)
#        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        self.assertTrue(len(response.content) > 1)
#        self.assertIn(b'access-granted',response.content)
#
#    @transaction.atomic
#    def test_profile_page_with_redirect_on_lockout(self):
#        # Pre-configure to lock the user out.
#        me = PublicMe.objects.get(owner=self.user)
#        me.is_locked = True
#        me.save()
#
#        # Run our test and verify.
#        url = reverse('tenant_profile')
#        response = self.authorized_client.get(url)
#        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
#        self.assertRedirects(response, reverse('tenant_profile_lock'))