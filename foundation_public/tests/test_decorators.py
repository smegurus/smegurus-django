from django.db import transaction
from django.contrib.auth.models import User
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_public.models.organization import PublicOrganization, PublicDomain
from foundation_public import constants


class FoundationPublicDecoratorWithPublicSchemaTestCase(TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Public Schema"""
        tenant.schema_name = 'test'
        tenant.name = "Galactic Alliance of Humankind"

    @transaction.atomic
    def setUp(self):
        super(FoundationPublicDecoratorWithPublicSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        super(FoundationPublicDecoratorWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_tenant_required_decorator_with_access_denied(self):
        response = self.c.get(reverse('tenant_is_valid'))
        self.assertEqual(response.status_code, 403)


class FoundationPublicDecoratorWithTenantSchemaTestCase(TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galactic'
        tenant.name = "Galactic Alliance of Humankind"

    @transaction.atomic
    def setUp(self):
        super(FoundationPublicDecoratorWithTenantSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        super(FoundationPublicDecoratorWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_tenant_required_decorator_with_access_granted(self):
        response = self.c.get(reverse('tenant_is_valid'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.content) > 1)
        self.assertIn(b'access-granted',response.content)
