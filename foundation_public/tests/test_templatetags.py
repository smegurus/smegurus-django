from django.utils import timezone
from datetime import datetime, timedelta
from django.db import transaction
from django.contrib.auth.models import User
from django.utils import translation
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_public.models.organization import PublicOrganization
from foundation_public.templatetags import foundation_public_tags
from smegurus import constants


class FoundationPublicTagsWithPublicSchemaTestCase(TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Public Schema"""
        tenant.schema_name = 'test'
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

    @transaction.atomic
    def setUp(self):
        super(FoundationPublicTagsWithPublicSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(FoundationPublicTagsWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_tenant_url_with_public_schema(self):
        url = foundation_public_tags.tenant_url(None, 'tenant_dashboard')
        self.assertIn(u'http://example.com/en/dashboard', url)


class FoundationPublicTagsWithTenantSchemaTestCase(TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galacticalliance'
        tenant.name = "Galactic Alliance of Humankind"
        tenant.has_perks=True
        tenant.has_mentors=True
        tenant.how_discovered = "Command HQ"
        tenant.how_many_served = 1

    @transaction.atomic
    def setUp(self):
        super(FoundationPublicTagsWithTenantSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(FoundationPublicTagsWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_tenant_url_with_tenant_schema(self):
        url = foundation_public_tags.tenant_url('galacticalliance', 'tenant_dashboard')
        self.assertIn(u'http://galacticalliance.example.com/en/dashboard', url)

    @transaction.atomic
    def test_pretty_formatted_date(self):
        today = timezone.now()
        pretty_text = foundation_public_tags.pretty_formatted_date(today)
        self.assertEqual(pretty_text, "Today")
