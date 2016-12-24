from django.db import models
from django.contrib.auth.models import User
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
        from django.contrib.sites.shortcuts import get_current_site # Reverse
        from django.core.urlresolvers import resolve, reverse # Reverse
        from django.contrib.sites.models import Site
        from smegurus.settings import env_var

        http_protocol = 'https://' if env_var("SECURE_SSL_REDIRECT") else 'http://'
        if self.schema_name:
            return http_protocol + self.schema_name + '.%s' % Site.objects.get_current().domain + reverse(view_name)
        else:
            return http_protocol + '%s' % Site.objects.get_current().domain + reverse(view_name)
