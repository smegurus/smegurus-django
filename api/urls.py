from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views
from api.views.authentication.login import LoginViewSet
from api.views.authentication.logout import LogoutViewSet
from api.views.authentication.register import RegisterViewSet
from api.views.authentication.emailactivation import EmailActivationView
from api.views.authentication.activation import ActivationView

from api.views.foundation_public.userviewset import UserViewSet
from api.views.foundation_public.userviewset import GroupViewSet
from api.views.foundation_public.publicfileuploadviewset import PublicFileUploadViewSet
from api.views.foundation_public.publicimageuploadviewset import PublicImageUploadViewSet
from api.views.foundation_public.languageviewset import PublicLanguageViewSet
from api.views.foundation_public.postaladdressviewset import PublicPostalAddressViewSet
from api.views.foundation_public.openinghoursspecificationviewset import PublicOpeningHoursSpecificationViewSet
from api.views.foundation_public.contactpointviewset import PublicContactPointViewSet
from api.views.foundation_public.geocoordinateviewset import PublicGeoCoordinateViewSet
from api.views.foundation_public.brandviewset import PublicBrandViewSet
from api.views.foundation_public.placeviewset import PublicPlaceViewSet
from api.views.foundation_public.countryviewset import PublicCountryViewSet
from api.views.foundation_public.organizationviewset import PublicOrganizationViewSet

from api.views.foundation_tenant.tenantfileuploadviewset import TenantFileUploadViewSet
from api.views.foundation_tenant.tenantimageuploadviewset import TenantImageUploadViewSet
from api.views.foundation_tenant.languageviewset import LanguageViewSet
from api.views.foundation_tenant.postaladdressviewset import PostalAddressViewSet
from api.views.foundation_tenant.openinghoursspecificationviewset import OpeningHoursSpecificationViewSet
from api.views.foundation_tenant.contactpointviewset import ContactPointViewSet
from api.views.foundation_tenant.geocoordinateviewset import GeoCoordinateViewSet
from api.views.foundation_tenant.brandviewset import BrandViewSet
from api.views.foundation_tenant.placeviewset import PlaceViewSet
from api.views.foundation_tenant.countryviewset import CountryViewSet
from api.views.foundation_tenant.meviewset import MeViewSet


# URL Generator.
router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'group', GroupViewSet)
router.register(r'publicfileupload', PublicFileUploadViewSet)
router.register(r'publicimageupload', PublicImageUploadViewSet)
router.register(r'publiclanguage', PublicLanguageViewSet)
router.register(r'publicpostaladdress', PublicPostalAddressViewSet)
router.register(r'publicopeninghoursspecification', PublicOpeningHoursSpecificationViewSet)
router.register(r'publiccontactpoint', PublicContactPointViewSet)
router.register(r'publicgeocoordinate', PublicGeoCoordinateViewSet)
router.register(r'publicbrand', PublicBrandViewSet)
router.register(r'publicplace', PublicPlaceViewSet)
router.register(r'publiccountry', PublicCountryViewSet)
router.register(r'publicorganization', PublicOrganizationViewSet)

router.register(r'tenantfileupload', TenantFileUploadViewSet)
router.register(r'tenantimageupload', TenantImageUploadViewSet)
router.register(r'tenantlanguage', LanguageViewSet)
router.register(r'tenantpostaladdress', PostalAddressViewSet)
router.register(r'tenantopeninghoursspecification', OpeningHoursSpecificationViewSet)
router.register(r'tenantcontactpoint', ContactPointViewSet)
router.register(r'tenantgeocoordinate', GeoCoordinateViewSet)
router.register(r'tenantbrand', BrandViewSet)
router.register(r'tenantplace', PlaceViewSet)
router.register(r'tenantcountry', CountryViewSet)
router.register(r'tenantme', MeViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = (
    url(r'^api/', include(router.urls)),  # Automatically generate the API for the registered models.

    # Manually set the authentication handling.
    url(r'^api/register/$', RegisterViewSet.as_view(), name='api_register'),
    url(r'^api/login/$', LoginViewSet.as_view(), name='api_login'),
    url(r'^api/logout/$', LogoutViewSet.as_view(), name='api_logout'),
    url(r'^api/emailactivation/$', EmailActivationView.as_view(), name='api_emailactivation'),
    url(r'^api/activate/$', ActivationView.as_view(), name='api_activate'),

    # Provide authentication for this API login app.
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Used for Token foundationd authentication.
    url(r'^api-token-auth/', views.obtain_auth_token),

    # All the functions with custom API.
    # url(r'^api/organization/$', OrganizationViewSet.as_view(), name='api_organization'),
)
