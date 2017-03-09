from django.contrib import admin
from foundation_public.models.banned import BannedDomain
from foundation_public.models.banned import SortedBannedIPByLatestCreationDate
from foundation_public.models.banned import BannedWord
from foundation_public.models.fileupload import PublicFileUpload
from foundation_public.models.imageupload import PublicImageUpload
from foundation_public.models.countryoption import CountryOption
from foundation_public.models.provinceoption import ProvinceOption
from foundation_public.models.cityoption import CityOption
from foundation_public.models.brand import PublicBrand
from foundation_public.models.contactpoint import PublicContactPoint
from foundation_public.models.geocoordinate import PublicGeoCoordinate
from foundation_public.models.language import PublicLanguage
from foundation_public.models.openinghoursspecification import PublicOpeningHoursSpecification
from foundation_public.models.postaladdress import PublicPostalAddress
from foundation_public.models.place import PublicPlace
from foundation_public.models.country import PublicCountry
from foundation_public.models.organizationregistration import PublicOrganizationRegistration
from foundation_public.models.organization import PublicOrganization
from foundation_public.models.organization import PublicDomain
from foundation_public.models.visitor import SortedPublicVisitorsByLatestCreation


# Register your models here.
admin.site.register(CountryOption)
admin.site.register(ProvinceOption)
admin.site.register(CityOption)
admin.site.register(BannedDomain)
admin.site.register(SortedBannedIPByLatestCreationDate)
admin.site.register(BannedWord)
admin.site.register(PublicFileUpload)
admin.site.register(PublicImageUpload)
admin.site.register(PublicBrand)
admin.site.register(PublicContactPoint)
admin.site.register(PublicGeoCoordinate)
admin.site.register(PublicLanguage)
admin.site.register(PublicOpeningHoursSpecification)
admin.site.register(PublicPostalAddress)
admin.site.register(PublicPlace)
admin.site.register(PublicCountry)
admin.site.register(PublicOrganization)
admin.site.register(PublicOrganizationRegistration)
admin.site.register(PublicDomain)
admin.site.register(SortedPublicVisitorsByLatestCreation)
