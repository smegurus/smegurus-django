from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views
from api.views.authentication.login import LoginViewSet
from api.views.authentication.logout import LogoutViewSet
from api.views.authentication.register import RegisterViewSet
from api.views.authentication.emailactivation import EmailActivationView
from api.views.authentication.activation import ActivationView
from api.views.organizationviewset import OrganizationViewSet
# # from api_tenant.views.foundation.userviewset import UserViewSet
# # from api_tenant.views.foundation.userviewset import GroupViewSet
# from api_tenant.views.foundation.meviewset import MeViewSet
from api.views.privatefileuploadviewset import PrivateFileUploadViewSet
from api.views.privateimageuploadviewset import PrivateImageUploadViewSet
from api.views.languageviewset import LanguageViewSet
from api.views.postaladdressviewset import PostalAddressViewSet
from api.views.openinghoursspecificationviewset import OpeningHoursSpecificationViewSet
from api.views.contactpointviewset import ContactPointViewSet
from api.views.geocoordinateviewset import GeoCoordinateViewSet
from foundation.views.publicfileuploadviewset import PublicFileUploadViewSet
from foundation.views.publicimageuploadviewset import PublicImageUploadViewSet

# URL Generator.
router = routers.DefaultRouter()

# Tenant Specific.
router.register(r'privatefileupload', PrivateFileUploadViewSet)
router.register(r'privateimageupload', PrivateImageUploadViewSet)
router.register(r'language', LanguageViewSet)
router.register(r'postaladdress', PostalAddressViewSet)
router.register(r'openinghoursspecification', OpeningHoursSpecificationViewSet)
router.register(r'geocoordinate', GeoCoordinateViewSet)
router.register(r'contactpoint', ContactPointViewSet)
# router.register(r'me', MeViewSet)

# Public Tenant.
# router.register(r'users', UserViewSet)
# router.register(r'groups', GroupViewSet)
router.register(r'publicfileupload', PublicFileUploadViewSet)
router.register(r'publicimageupload', PublicImageUploadViewSet)

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
    url(r'^api/organization/$', OrganizationViewSet.as_view(), name='api_organization'),
)
