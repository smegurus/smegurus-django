from django.contrib import admin
from foundation_public.models.banned import BannedDomain
from foundation_public.models.banned import BannedIP
from foundation_public.models.banned import BannedWord
from foundation_public.models.fileupload import PublicFileUpload
from foundation_public.models.imageupload import PublicImageUpload
from foundation_public.models.brand import PublicBrand
from foundation_public.models.contactpoint import PublicContactPoint
from foundation_public.models.geocoordinate import PublicGeoCoordinate
from foundation_public.models.language import PublicLanguage
from foundation_public.models.openinghoursspecification import PublicOpeningHoursSpecification
from foundation_public.models.postaladdress import PublicPostalAddress
from foundation_public.models.place import PublicPlace
from foundation_public.models.country import PublicCountry
from foundation_public.models.organization import PublicOrganization
from foundation_public.models.organization import Domain


# Register your models here.
admin.site.register(BannedDomain)
admin.site.register(BannedIP)
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
admin.site.register(Domain)
