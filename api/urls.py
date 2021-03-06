from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views

# PUBLIC
from api.views.authentication.login import LoginViewSet
from api.views.authentication.logout import LogoutViewSet
from api.views.authentication.register import RegisterViewSet
from api.views.authentication.emailactivation import EmailActivationView
from api.views.authentication.activation import ActivationView
from api.views.authentication.emailpasswordreset import EmailPasswordResetViewSet
from api.views.authentication.changepassword import ChangePasswordViewSet
from api.views.foundation_public.publicfileuploadviewset import PublicFileUploadViewSet
from api.views.foundation_public.publicimageuploadviewset import PublicImageUploadViewSet
from api.views.foundation_public.countryoptionviewset import PublicCountryOptionViewSet
from api.views.foundation_public.provinceoptionviewset import PublicProvinceOptionViewSet
from api.views.foundation_public.cityoptionviewset import PublicCityOptionViewSet
from api.views.foundation_public.languageviewset import PublicLanguageViewSet
from api.views.foundation_public.postaladdressviewset import PublicPostalAddressViewSet
from api.views.foundation_public.openinghoursspecificationviewset import PublicOpeningHoursSpecificationViewSet
from api.views.foundation_public.contactpointviewset import PublicContactPointViewSet
from api.views.foundation_public.geocoordinateviewset import PublicGeoCoordinateViewSet
from api.views.foundation_public.brandviewset import PublicBrandViewSet
from api.views.foundation_public.placeviewset import PublicPlaceViewSet
from api.views.foundation_public.countryviewset import PublicCountryViewSet
from api.views.foundation_public.organizationregistrationviewset import PublicOrganizationRegistrationViewSet
from api.views.foundation_public.organizationviewset import PublicOrganizationViewSet
from api.views.foundation_public.functionviewset import IsEmailUniqueViewSet
from api.views.foundation_public.functionviewset import IsOrganizationSchemaNameUniqueViewSet

# TENANT - BASE
from api.views.foundation_tenant_base.tenantfileuploadviewset import FileUploadViewSet
from api.views.foundation_tenant_base.tenantimageuploadviewset import ImageUploadViewSet
from api.views.foundation_tenant_base.countryoptionviewset import TenantCountryOptionViewSet
from api.views.foundation_tenant_base.provinceoptionviewset import TenantProvinceOptionViewSet
from api.views.foundation_tenant_base.cityoptionviewset import TenantCityOptionViewSet
from api.views.foundation_tenant_base.naicsoptionviewset import NAICSOptionViewSet
from api.views.foundation_tenant_base.languageviewset import LanguageViewSet
from api.views.foundation_tenant_base.postaladdressviewset import PostalAddressViewSet
from api.views.foundation_tenant_base.openinghoursspecificationviewset import OpeningHoursSpecificationViewSet
from api.views.foundation_tenant_base.contactpointviewset import ContactPointViewSet
from api.views.foundation_tenant_base.geocoordinateviewset import GeoCoordinateViewSet
from api.views.foundation_tenant_base.brandviewset import BrandViewSet
from api.views.foundation_tenant_base.placeviewset import PlaceViewSet
from api.views.foundation_tenant_base.countryviewset import CountryViewSet
from api.views.foundation_tenant_base.tagviewset import TagViewSet
from api.views.foundation_tenant_base.businessideaviewset import BusinessIdeaViewSet
from api.views.foundation_tenant_base.tellusyourneedviewset import TellUsYourNeedViewSet
from api.views.foundation_tenant_base.calendareventviewset import CalendarEventViewSet
from api.views.foundation_tenant_base.intakeviewset import IntakeViewSet
from api.views.foundation_tenant_base.admissionviewset import AdmissionViewSet
from api.views.foundation_tenant_base.faqgroupviewset import FAQGroupViewSet
from api.views.foundation_tenant_base.faqitemviewset import FAQItemViewSet
from api.views.foundation_tenant_base.communitypostviewset import CommunityPostViewSet
from api.views.foundation_tenant_base.communityadvertisementviewset import CommunityAdvertisementViewSet
from api.views.foundation_tenant_base.messageviewset import MessageViewSet
from api.views.foundation_tenant_base.noteviewset import NoteViewSet
from api.views.foundation_tenant_base.taskviewset import TaskViewSet
from api.views.foundation_tenant_base.inforesourcecategoryviewset import InfoResourceCategoryViewSet
from api.views.foundation_tenant_base.inforesourceviewset import InfoResourceViewSet
from api.views.foundation_tenant_base.functionviewset import FinalizeTenantSetupFunctionViewSet
from api.views.foundation_tenant_base.meviewset import MeViewSet
from api.views.foundation_tenant_base.notificationviewset import NotificationViewSet

# TENANT - BIZMULA
from api.views.foundation_tenant_bizmula.workspaceviewset import WorkspaceViewSet
from api.views.foundation_tenant_bizmula.moduleviewset import ModuleViewSet
from api.views.foundation_tenant_bizmula.questionviewset import QuestionViewSet
from api.views.foundation_tenant_bizmula.questionanswerviewset import QuestionAnswerViewSet
from api.views.foundation_tenant_bizmula.documenttypeviewset import DocumentTypeViewSet
from api.views.foundation_tenant_bizmula.documentviewset import DocumentViewSet

# URL Generator.
# PUBLIC
router = routers.DefaultRouter()
router.register(r'publicfileupload', PublicFileUploadViewSet)
router.register(r'publicimageupload', PublicImageUploadViewSet)
router.register(r'publiccountryoption', PublicCountryOptionViewSet)
router.register(r'publicprovinceoption', PublicProvinceOptionViewSet)
router.register(r'publiccityoption', PublicCityOptionViewSet)
router.register(r'publiclanguage', PublicLanguageViewSet)
router.register(r'publicpostaladdress', PublicPostalAddressViewSet)
router.register(r'publicopeninghoursspecification', PublicOpeningHoursSpecificationViewSet)
router.register(r'publiccontactpoint', PublicContactPointViewSet)
router.register(r'publicgeocoordinate', PublicGeoCoordinateViewSet)
router.register(r'publicbrand', PublicBrandViewSet)
router.register(r'publicplace', PublicPlaceViewSet)
router.register(r'publiccountry', PublicCountryViewSet)
router.register(r'publicorganizationregistration', PublicOrganizationRegistrationViewSet)
router.register(r'publicorganization', PublicOrganizationViewSet)

# TENANT - BASE
router.register(r'tenantfileupload', FileUploadViewSet)
router.register(r'tenantimageupload', ImageUploadViewSet)
router.register(r'tenantcountryoption', TenantCountryOptionViewSet)
router.register(r'tenantprovinceoption', TenantProvinceOptionViewSet)
router.register(r'tenantcityoption', TenantCityOptionViewSet)
router.register(r'tenantnaicsoption', NAICSOptionViewSet)
router.register(r'tenantlanguage', LanguageViewSet)
router.register(r'tenantpostaladdress', PostalAddressViewSet)
router.register(r'tenantopeninghoursspecification', OpeningHoursSpecificationViewSet)
router.register(r'tenantcontactpoint', ContactPointViewSet)
router.register(r'tenantgeocoordinate', GeoCoordinateViewSet)
router.register(r'tenantbrand', BrandViewSet)
router.register(r'tenantplace', PlaceViewSet)
router.register(r'tenantcountry', CountryViewSet)
router.register(r'tenanttag', TagViewSet)
router.register(r'tenantbusinessidea', BusinessIdeaViewSet)
router.register(r'tenanttellusyourneed', TellUsYourNeedViewSet)
router.register(r'tenantcalendarevent', CalendarEventViewSet)
router.register(r'tenantcalendarevent', CalendarEventViewSet)
router.register(r'tenantintake', IntakeViewSet)
router.register(r'tenantadmission', AdmissionViewSet)
router.register(r'tenantfaqgroup', FAQGroupViewSet)
router.register(r'tenantfaqitem', FAQItemViewSet)
router.register(r'tenantcommunitypost', CommunityPostViewSet)
router.register(r'tenantcommunityadvertisement', CommunityAdvertisementViewSet)
router.register(r'tenantmessage', MessageViewSet)
router.register(r'tenantnote', NoteViewSet)
router.register(r'tenantnotification', NotificationViewSet)
router.register(r'tenanttask', TaskViewSet)
router.register(r'tenantinforesourcecategory', InfoResourceCategoryViewSet)
router.register(r'tenantinforesource', InfoResourceViewSet)
router.register(r'tenantme', MeViewSet)

# TENANT - BIZMULA
router.register(r'tenantworkspace', WorkspaceViewSet)
router.register(r'tenantmodule', ModuleViewSet)
router.register(r'tenantdocumenttype', DocumentTypeViewSet)
router.register(r'tenantdocument', DocumentViewSet)
router.register(r'tenantquestion', QuestionViewSet)
router.register(r'tenantquestionanswer', QuestionAnswerViewSet)

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
    url(r'^api/emailpasswordreset/$', EmailPasswordResetViewSet.as_view(), name='api_emailpasswordreset'),
    url(r'^api/changepassword/$', ChangePasswordViewSet.as_view(), name='api_changepassword'),

    # Custom Functions.
    url(r'^api/isemailunique/$', IsEmailUniqueViewSet.as_view(), name='api_function_isemailunique'),
    url(r'^api/isorganizationschemanameunique/$', IsOrganizationSchemaNameUniqueViewSet.as_view(), name='api_function_is_organization_schema_name_unique'),
    url(r'^api/finalize_tenant/$', FinalizeTenantSetupFunctionViewSet.as_view(), name='api_function_finalize_tenant'),

    # Provide authentication for this API login app.
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Used for Token foundationd authentication.
    url(r'^api-token-auth/', views.obtain_auth_token),

    # All the functions with custom API.
    # url(r'^api/organization/$', OrganizationViewSet.as_view(), name='api_organization'),
)
