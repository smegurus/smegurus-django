from django.utils import timezone
from datetime import datetime, timedelta
from django.db import transaction
from django.contrib.auth.models import User
from django.utils import translation
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from rest_framework.test import APITestCase
from foundation_public.models.organization import PublicOrganization, PublicDomain
from foundation_public.templatetags.foundation_public_tags import tenant_url
from foundation_public.utils import get_unique_username_from_email
from foundation_public.utils import get_pretty_formatted_date
from foundation_public.utils import latest_date_between
from foundation_public.utils import latest_date_in
from foundation_public.utils import random_text
from smegurus import constants


class FoundationPublicUtilsTestCase(APITestCase):
    fixtures = []

    @transaction.atomic
    def setUp(self):
        pass

    @transaction.atomic
    def tearDown(self):
        pass
        # users = User.objects.all()
        # for user in users.all():
        #     user.delete()
        # super(FoundationPublicUtilsWithPublicSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_get_unique_username_from_email(self):
        random_text = get_unique_username_from_email("ledo@galacticalliance.com")
        self.assertTrue(len(random_text) > 1)

    @transaction.atomic
    def test_get_pretty_formatted_date(self):
        today = timezone.now()
        # - - - - - - - - - - - - - - - - - -
        # CASE 1 OF 4: None
        # - - - - - - - - - - - - - - - - - -
        pretty_text = get_pretty_formatted_date(None)
        self.assertEqual(pretty_text, "-")

        # - - - - - - - - - - - - - - - - - -
        # CASE 2 OF 4: Today
        # - - - - - - - - - - - - - - - - - -
        pretty_text = get_pretty_formatted_date(today)
        self.assertEqual(pretty_text, "Today")

        # - - - - - - - - - - - - - - - - - -
        # CASE 3 OF 4: Between 0 to 60 days
        # - - - - - - - - - - - - - - - - - -
        N = 45
        dt = today - timedelta(days=N)
        pretty_text = get_pretty_formatted_date(dt)
        self.assertEqual(pretty_text, "45 days ago")

        # - - - - - - - - - - - - - - - - - -
        # CASE 4 OF 4: After 60 days
        # - - - - - - - - - - - - - - - - - -
        N = 128
        dt = today - timedelta(days=N)
        pretty_text = get_pretty_formatted_date(dt)
        self.assertTrue(len(pretty_text) > 1)

    @transaction.atomic
    def test_latest_date_between(self):
        today = timezone.now()
        N = 45
        dt = today - timedelta(days=N)

        # - - - - - - #
        # CASE 1 OF 2 #
        # - - - - - - #
        latest = latest_date_between(today, dt)
        self.assertEqual(today, latest);

        # - - - - - - #
        # CASE 2 OF 2 #
        # - - - - - - #
        latest = latest_date_between(dt, today)
        self.assertEqual(today, latest);

    @transaction.atomic
    def test_latest_date_in(self):
        today = timezone.now()
        date_1 = today - timedelta(days=45)
        date_2 = today - timedelta(days=365)
        date_3 = today - timedelta(days=720)
        date_4 = today - timedelta(days=32)
        date_5 = today - timedelta(days=2)
        latest_date = latest_date_in([
            date_3, date_2, today, date_1, date_4, date_5
        ])
        self.assertEqual(today, latest_date)

    @transaction.atomic
    def test_random_text(self):
        text = random_text(31)
        self.assertTrue(len(text) > 0)
