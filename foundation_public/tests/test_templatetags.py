from django.db import transaction
from django.contrib.auth.models import User
from django.utils import translation
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_public.models.organization import PublicOrganization, PublicDomain
from foundation_public import constants
from foundation_public.templatetags.foundation_public_tags import tenant_url


class FoundationPublicTagsWithPublicSchemaTestCase(TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Public Schema"""
        tenant.schema_name = 'test'
        tenant.name = "Galactic Alliance of Humankind"

    @transaction.atomic
    def setUp(self):
        super(FoundationPublicTagsWithPublicSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        super(FoundationPublicTagsWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_tenant_url_with_public_schema(self):
        url = tenant_url(None, 'tenant_dashboard')
        self.assertIn(u'http://example.com/en/dashboard', url)


class FoundationPublicTagsWithTenantSchemaTestCase(TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galacticalliance'
        tenant.name = "Galactic Alliance of Humankind"

    @transaction.atomic
    def setUp(self):
        super(FoundationPublicTagsWithTenantSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        super(FoundationPublicTagsWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_tenant_url_with_tenant_schema(self):
        url = tenant_url('galacticalliance', 'tenant_dashboard')
        self.assertIn(u'http://galacticalliance.example.com/en/dashboard', url)
