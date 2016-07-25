from django.db import transaction
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import resolve, reverse
from django.utils import translation
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_tenant.models.me import TenantMe
from foundation_public import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRSTNAME = "Ledo"
TEST_USER_LASTNAME = ""


class FoundationTenantMiddlewareWithPublicSchemaTestCase(APITestCase, TenantTestCase):
    """
    DEVELOPERS NOTE:
        - This unit test is dependent on the "public_index" app.
    """
    fixtures = []

    def setup_tenant(self, tenant):
        """Public Schema"""
        tenant.schema_name = 'test'
        tenant.name = "Galactic Alliance of Humankind"

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

    @transaction.atomic
    def setUp(self):
        super(FoundationTenantMiddlewareWithPublicSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        items = User.objects.all()
        for item in items.all():
            item.delete()
        TenantMe.objects.delete_all()
        super(FoundationTenantMiddlewareWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_tenantmemiddleware_with_unauthenticated_user_in_public_schema(self):
        # Verify that no "Me" objects are created.
        self.assertEqual(TenantMe.objects.all().count(), 0)

        # Run the test.
        client = TenantClient(self.tenant)
        response = client.get(reverse('public_index'))
        self.assertEqual(response.status_code, 200)

        # Verify that no "Me" objects are created.
        self.assertEqual(TenantMe.objects.all().count(), 0)


    @transaction.atomic
    def test_tenantmemiddleware_with_authenticated_user_in_public_schema(self):
        # Verify that no "Me" objects are created.
        self.assertEqual(TenantMe.objects.all().count(), 0)

        # Create our User and run our test.
        user = User.objects.create_user(  # Create our User.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD,
            first_name=TEST_USER_FIRSTNAME,
            last_name=TEST_USER_LASTNAME,
        )
        user.is_active = True
        user.save()
        token = Token.objects.get(user=user)
        client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get(reverse('public_index'))
        self.assertEqual(response.status_code, 200)

        # Verify
        me = TenantMe.objects.get_by_owner_or_none(owner=user)
        self.assertIsNone(me)



class FoundationTenantMiddlewareWithTenantSchemaTestCase(APITestCase, TenantTestCase):
    """
    DEVELOPERS NOTE:
        - This unit test is dependent on the "public_index" app.
    """
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galacticalliance'
        tenant.name = "Galactic Alliance of Humankind"

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

    @transaction.atomic
    def setUp(self):
        super(FoundationTenantMiddlewareWithTenantSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        #super(FoundationTenantMiddlewareWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_tenantmemiddleware_with_unauthenticated_user_in_tenant_schema(self):
        # Verify that no "Me" objects are created.
        self.assertEqual(TenantMe.objects.all().count(), 0)

        # Run the test.
        client = TenantClient(self.tenant)
        response = client.get(reverse('public_index'))
        self.assertEqual(response.status_code, 200)

        # Verify that no "Me" objects are created.
        self.assertEqual(TenantMe.objects.all().count(), 0)


    @transaction.atomic
    def test_tenantmemiddleware_with_authenticated_user_in_tenant_schema(self):
        # Verify that no "Me" objects are created.
        self.assertEqual(TenantMe.objects.all().count(), 0)

        # Create our User and run our test.
        user = User.objects.create_user(  # Create our User.
            email=TEST_USER_EMAIL,
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD,
            first_name=TEST_USER_FIRSTNAME,
            last_name=TEST_USER_LASTNAME,
        )
        user.is_active = True
        user.save()
        token = Token.objects.get(user=user)
        client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)
        client.login(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD
        )
        response = client.get(reverse('public_index'))
        self.assertEqual(response.status_code, 200)

        # Verify
        me = TenantMe.objects.get_by_owner_or_none(owner=user)
        self.assertIsNotNone(me)
