import json
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
from api.views import authentication
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.postaladdress import PostalAddress
from foundation_tenant.models.contactpoint import ContactPoint
from foundation_tenant.models.countryoption import CountryOption
from foundation_tenant.models.provinceoption import ProvinceOption
from foundation_tenant.models.cityoption import CityOption
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"


class APIPostalAdressWithTenantSchemaTestCase(APITestCase, TenantTestCase):
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
        super(APIPostalAdressWithTenantSchemaTestCase, self).setUp()

        # Initialize our test data.
        self.user = User.objects.get()
        token = Token.objects.get(user__username=TEST_USER_USERNAME)

        # Setup.
        self.unauthorized_client = TenantClient(self.tenant)
        self.authorized_client = TenantClient(self.tenant, HTTP_AUTHORIZATION='Token ' + token.key)

        # Above taken from:
        # http://www.django-rest-framework.org/api-guide/testing/#authenticating

    @transaction.atomic
    def tearDown(self):
        CountryOption.objects.delete_all()
        ProvinceOption.objects.delete_all()
        CityOption.objects.delete_all()
        PostalAddress.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        # super(APIPostalAdressWithTenantSchemaTestCase, self).tearDown()

    @transaction.atomic
    def test_list(self):
        response = self.unauthorized_client.get('/api/tenantpostaladdress/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_list_with_authentication(self):
        response = self.authorized_client.get('/api/tenantpostaladdress/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_post(self):
        country = CountryOption.objects.create(
            id=1,
            name="Avalon"
        )
        province = ProvinceOption.objects.create(
            id=1,
            country=country,
            name="Colony Ship #124"
        )
        city = CityOption.objects.create(
            id=1,
            country=country,
            province=province,
            name="District 9"
        )
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'country': country.id,
            'region': province.id,
            'locality': city.name
        }
        response = self.unauthorized_client.post('/api/tenantpostaladdress/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_post_with_authentication(self):
        country = CountryOption.objects.create(
            id=1,
            name="Avalon"
        )
        province = ProvinceOption.objects.create(
            id=1,
            country=country,
            name="Colony Ship #124"
        )
        city = CityOption.objects.create(
            id=1,
            country=country,
            province=province,
            name="District 9"
        )
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'country': country.id,
            'region': province.id,
            'locality': city.name
        }
        response = self.authorized_client.post('/api/tenantpostaladdress/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @transaction.atomic
    def test_put(self):
        country = CountryOption.objects.create(
            id=1,
            name="Avalon"
        )
        province = ProvinceOption.objects.create(
            id=1,
            country=country,
            name="Sector 666"
        )
        city = CityOption.objects.create(
            id=1,
            country=country,
            province=province,
            name="District 9"
        )
        PostalAddress.objects.create(
            id=1,
            name="Unit Test",
            description="Used for unit testing purposes.",
            owner=self.user,
            country=country,
            region=province,
            locality=city.name,
        )

        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'country': country.id,
            'region': province.id,
            'locality': city.name
        }
        response = self.unauthorized_client.put('/api/tenantpostaladdress/1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_put_with_authorization(self):
        country = CountryOption.objects.create(
            id=1,
            name="Avalon"
        )
        province = ProvinceOption.objects.create(
            id=1,
            country=country,
            name="Sector 666"
        )
        city = CityOption.objects.create(
            id=1,
            country=country,
            province=province,
            name="District 9"
        )
        PostalAddress.objects.create(
            id=1,
            name="Unit Test",
            description="Used for unit testing purposes.",
            owner=self.user,
            country=country,
            region=province,
            locality=city.name,
        )
        data = {
            'name': 'Unit Test',
            'description': 'Used for unit testing purposes.',
            'owner': self.user.id,
            'country': country.id,
            'region': province.id,
            'locality': city.name
        }
        response = self.authorized_client.put('/api/tenantpostaladdress/1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @transaction.atomic
    def test_delete(self):
        country = CountryOption.objects.create(
            id=1,
            name="Avalon"
        )
        province = ProvinceOption.objects.create(
            id=1,
            country=country,
            name="Sector 666"
        )
        city = CityOption.objects.create(
            id=1,
            country=country,
            province=province,
            name="District 9"
        )
        PostalAddress.objects.create(
            id=1,
            name="Unit Test",
            description="Used for unit testing purposes.",
            owner=self.user,
            country=country,
            region=province,
            locality=city.name,
        )
        response = self.unauthorized_client.delete('/api/tenantpostaladdress/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_delete_with_authentication(self):
        country = CountryOption.objects.create(
            id=1,
            name="Avalon"
        )
        province = ProvinceOption.objects.create(
            id=1,
            country=country,
            name="Sector 666"
        )
        city = CityOption.objects.create(
            id=1,
            country=country,
            province=province,
            name="District 9"
        )
        PostalAddress.objects.create(
            id=1,
            name="Unit Test",
            description="Used for unit testing purposes.",
            owner=self.user,
            country=country,
            region=province,
            locality=city.name,
        )
        response = self.authorized_client.delete('/api/tenantpostaladdress/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def test_rebuild_geo_data_with_anonymous_user(self):
        # Create a new object with our specific test data.
        country = CountryOption.objects.create(
            id=1,
            name='Ontario',
        )
        region = ProvinceOption.objects.create(
            id=1,
            name='Canada',
            country=country
        )
        PostalAddress.objects.create(
            id=1,
            name='Test Address',
            owner=self.user,
            street_number='120',
            street_name='Centre',
            street_type='ST',
            suite_number='102',
            postal_code='N6J4X4',
            locality='London',
            region=region,
            country=country,
        )

        # Run the test.
        response = self.unauthorized_client.put(
            '/api/tenantpostaladdress/1/rebuild_geo_data/?format=json',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @transaction.atomic
    def test_rebuild_geo_data_with_authenticated_user(self):
        # Create a new object with our specific test data.
        country = CountryOption.objects.create(
            id=1,
            name='Ontario',
        )
        region = ProvinceOption.objects.create(
            id=1,
            name='Canada',
            country=country
        )
        PostalAddress.objects.create(
            id=1,
            name='Test Address',
            owner=self.user,
            street_number='120',
            street_name='Centre',
            street_type='ST',
            suite_number='102',
            postal_code='N6J4X4',
            locality='London',
            region=region,
            country=country,
        )

        # Run the test.
        response = self.authorized_client.put(
            '/api/tenantpostaladdress/1/rebuild_geo_data/?format=json',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
