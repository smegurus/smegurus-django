from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_tenants.models import TenantMixin, DomainMixin
from smegurus import constants
from foundation_public.models.abstract_thing import AbstractPublicThing
from foundation_public.models.imageupload import PublicImageUpload
from foundation_public.models.brand import PublicBrand
from foundation_public.models.contactpoint import PublicContactPoint
from foundation_public.models.geocoordinate import PublicGeoCoordinate
from foundation_public.models.language import PublicLanguage
from foundation_public.models.openinghoursspecification import PublicOpeningHoursSpecification
from foundation_public.models.postaladdress import PublicPostalAddress
from foundation_public.models.place import PublicPlace


class PublicOrganizationRegistration(AbstractPublicThing):
    class Meta:
        app_label = 'foundation_public'
        db_table = 'smeg_organization_registration'
        verbose_name = 'Organization Registration'
        verbose_name_plural = 'Organizations Registration'

    schema_name = models.CharField(
        _("Legal Name"),
        max_length=255,
        help_text=_('The official name of the organization, e.g. the registered company name.'),
        blank=True,
        null=True,
    )
    name = models.CharField(
        _("Legal Name"),
        max_length=255,
        help_text=_('The official name of the organization, e.g. the registered company name.'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)

    def reverse(self, view_name):
        """
        Reverse the URL of the request + view name for this Organization.
        """
        if self.schema_name:
            return settings.SMEGURUS_APP_HTTP_PROTOCOL + self.schema_name + '.%s' % settings.SMEGURUS_APP_HTTP_DOMAIN + reverse(view_name)
        else:
            return settings.SMEGURUS_APP_HTTP_PROTOCOL + '%s' % settings.SMEGURUS_APP_HTTP_DOMAIN + reverse(view_name)
