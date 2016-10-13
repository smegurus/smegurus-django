from django.utils import timezone
from datetime import datetime, timedelta
from django.db import transaction
from django.contrib.auth.models import User
from django.utils import translation
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_tenant.utils import my_last_modified_func
from foundation_tenant.utils import get_pretty_formatted_date
from foundation_tenant.utils import int_or_none
from smegurus import constants


class FoundationTenantUtilsWithTenantSchemaTestCase(TenantTestCase):
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
        super(FoundationTenantUtilsWithTenantSchemaTestCase, self).setUp()
        self.c = TenantClient(self.tenant)

    @transaction.atomic
    def tearDown(self):
        users = User.objects.all()
        for user in users.all():
            user.delete()
        super(FoundationTenantUtilsWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_my_last_modified_func(self):
        pass  #TODO: Implement.

    @transaction.atomic
    def test_get_pretty_formatted_date(self):
        today = timezone.now()

        # - - - - - - - - - - - - - - - - - -
        # CASE 1 OF 3: Today
        # - - - - - - - - - - - - - - - - - -
        pretty_text = get_pretty_formatted_date(today)
        self.assertEqual(pretty_text, "Today")

        # - - - - - - - - - - - - - - - - - -
        # CASE 2 OF 3: Between 0 to 60 days
        # - - - - - - - - - - - - - - - - - -
        N = 45
        dt = today - timedelta(days=N)
        pretty_text = get_pretty_formatted_date(dt)
        self.assertEqual(pretty_text, "45 days ago")

        # - - - - - - - - - - - - - - - - - -
        # CASE 3 OF 3: After 60 days
        # - - - - - - - - - - - - - - - - - -
        N = 128
        dt = today - timedelta(days=N)
        pretty_text = get_pretty_formatted_date(dt)
        self.assertTrue(len(pretty_text) > 1)

    @transaction.atomic
    def test_int_or_none(self):
        # Case 1 of 2:
        value = int_or_none('3')
        self.assertEqual(value, 3)

        # Case 2 of 2:
        value = int_or_none('')
        self.assertIsNone(value)
