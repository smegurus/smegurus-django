from django.db import transaction
from django.contrib.auth.models import User, Group
from django.utils import translation
from django.core.urlresolvers import resolve, reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from foundation_tenant.models.base.governmentbenefitoption import GovernmentBenefitOption
from foundation_tenant.models.base.identifyoption import IdentifyOption
from foundation_tenant.models.base.countryoption import CountryOption
from foundation_tenant.models.base.provinceoption import ProvinceOption
from foundation_tenant.models.base.cityoption import CityOption
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.postaladdress import PostalAddress
from foundation_tenant.models.base.contactpoint import ContactPoint
from foundation_tenant.models.base.intake import Intake
from smegurus import constants


TEST_USER_EMAIL = "ledo@gah.com"
TEST_USER_USERNAME = "Ledo"
TEST_USER_PASSWORD = "GalacticAllianceOfHumankind"
TEST_USER_FIRST_NAME = "Ledo"
TEST_USER_LAST_NAME = ""


class TenantIntakeEntrepreneurTestCases(APITestCase, TenantTestCase):
    fixtures = []

    def setup_tenant(self, tenant):
        """Tenant Schema"""
        tenant.schema_name = 'galacticalliance'
        tenant.name = "Galactic Alliance of Humankind"
        tenant.is_setup = True
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
            password=TEST_USER_PASSWORD
        )
        user.is_active = True
        user.save()

    @transaction.atomic
    def setUp(self):
        translation.activate('en')  # Set English
        super(TenantIntakeEntrepreneurTestCases, self).setUp()
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
        country = CountryOption.objects.create(id=1, name='Avalan')
        province = ProvinceOption.objects.create(id=1, name='Colony 01', country=country)
        city = CityOption.objects.create(id=1, name='Megazone 23', province=province, country=country,)
        self.me = Me.objects.create(
            owner=self.user,
            address=PostalAddress.objects.create(
                country=CountryOption.objects.get(id=1),
                region=ProvinceOption.objects.get(id=1),
                locality=CityOption.objects.get(id=1),
                owner=self.user
            )
        )

        # Make the User belong to the Entrepreneur group.
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.add(entrepreneur_group)
        self.user.save()

        # Create the Intake object.
        intake = Intake.objects.create(
            me=self.me,
            status=constants.CREATED_STATUS
        )

    @transaction.atomic
    def tearDown(self):
        PostalAddress.objects.delete_all()
        ContactPoint.objects.delete_all()
        Me.objects.delete_all()
        users = User.objects.all()
        for user in users.all():
            user.delete()
        items = Group.objects.all()
        for item in items.all():
            item.delete()
        # super(TenantIntakeEntrepreneurTestCases, self).tearDown()

    @transaction.atomic
    def test_intake_page_with_employee_user(self):
        entrepreneur_group = Group.objects.get(id=constants.ENTREPRENEUR_GROUP_ID)
        self.user.groups.remove(entrepreneur_group)
        self.user.save()

        url = reverse('tenant_intake_entr_round_one_step_one')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @transaction.atomic
    def test_intake_round_one_page_one_with_entrepreneur_user(self):
        url = reverse('tenant_intake_entr_round_one_step_one')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        #self.assertIn(b'Rewards',response.content)

    @transaction.atomic
    def test_intake_round_one_page_two_with_entrepreneur_user(self):
        url = reverse('tenant_intake_entr_round_one_step_two')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        #self.assertIn(b'Rewards',response.content)

    @transaction.atomic
    def test_intake_round_one_page_three_with_entrepreneur_user(self):
        url = reverse('tenant_intake_entr_round_one_step_three')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        #self.assertIn(b'Rewards',response.content)

    @transaction.atomic
    def test_intake_round_one_page_four_with_entrepreneur_user(self):
        url = reverse('tenant_intake_entr_round_one_step_four')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        #self.assertIn(b'Rewards',response.content)

    @transaction.atomic
    def test_intake_round_one_page_five_with_entrepreneur_user(self):
        url = reverse('tenant_intake_entr_round_one_step_five')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        #self.assertIn(b'Rewards',response.content)

    @transaction.atomic
    def test_intake_round_one_page_six_with_entrepreneur_user(self):
        url = reverse('tenant_intake_entr_round_one_step_six')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        #self.assertIn(b'Rewards',response.content)

    @transaction.atomic
    def test_intake_round_two_page_one_with_entrepreneur_user(self):
        url = reverse('tenant_intake_entr_round_two_step_one')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        #self.assertIn(b'Rewards',response.content)

    @transaction.atomic
    def test_intake_round_two_page_two_with_entrepreneur_user(self):
        url = reverse('tenant_intake_entr_round_two_step_two')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        #self.assertIn(b'Rewards',response.content)

    @transaction.atomic
    def test_intake_round_two_page_three_with_entrepreneur_user(self):
        url = reverse('tenant_intake_entr_round_two_step_three')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        #self.assertIn(b'Rewards',response.content)

    @transaction.atomic
    def test_intake_round_two_page_four_with_entrepreneur_user(self):
        url = reverse('tenant_intake_entr_round_two_step_four')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        #self.assertIn(b'Rewards',response.content)

    @transaction.atomic
    def test_intake_round_two_page_five_with_entrepreneur_user(self):
        url = reverse('tenant_intake_entr_round_two_step_five')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        #self.assertIn(b'Rewards',response.content)

    @transaction.atomic
    def test_intake_finished_page_with_entrepreneur_user(self):
        url = reverse('tenant_intake_finished')
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.content) > 1)
        #self.assertIn(b'Rewards',response.content)
