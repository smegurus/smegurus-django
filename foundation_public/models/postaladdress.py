from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.abstract_thing import AbstractPublicThing
from foundation_public.models.countryoption import CountryOption
from foundation_public.models.provinceoption import ProvinceOption
from foundation_public.models.cityoption import CityOption


class PublicPostalAddressManager(models.Manager):
    def delete_all(self):
        items = PublicPostalAddress.objects.all()
        for item in items.all():
            item.delete()


class PublicPostalAddress(AbstractPublicThing):
    """
    The mailing address.

    https://schema.org/PostalAddress
    """
    class Meta:
        app_label = 'foundation_public'
        db_table = 'biz_postal_addresses'
        verbose_name = 'Postal Address'
        verbose_name_plural = 'Postal Addresses'

    objects = PublicPostalAddressManager()
    address_country = models.ForeignKey(
        CountryOption,
        help_text=_('The country. For example, USA. You can also provide the two-letter <a href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements">ISO 3166-1 alpha-2</a> country code.'),
        null=True,
        blank=True,
        related_name="postaladdress_country_%(app_label)s_%(class)s_related",
        db_index=True,
        on_delete=models.CASCADE
    )
    address_locality = models.ForeignKey(
        CityOption,
        help_text=_('The locality. For example, Mountain View.'),
        null=True,
        blank=True,
        related_name="postaladdress_city_%(app_label)s_%(class)s_related",
        db_index=True,
        on_delete=models.CASCADE
    )
    address_region = models.ForeignKey(
        ProvinceOption,
        help_text=_('The region. For example, CA.'),
        null=True,
        blank=True,
        related_name="postaladdress_province_%(app_label)s_%(class)s_related",
        db_index=True,
        on_delete=models.CASCADE
    )
    post_office_box_number = models.CharField(
        _("Post Office Box Number"),
        max_length=127,
        help_text=_('The post office box number for PO box addresses.'),
        blank=True,
        null=True,
    )
    postal_code = models.CharField(
        _("Postal Code"),
        max_length=127,
        help_text=_('The postal code. For example, 94043.'),
        blank=True,
        null=True,
    )
    street_address = models.CharField(
        _("Street Address"),
        max_length=255,
        help_text=_('The street address. For example, 1600 Amphitheatre Pkwy.'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)
