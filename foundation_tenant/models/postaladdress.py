from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.countryoption import CountryOption
from foundation_tenant.models.provinceoption import ProvinceOption
from foundation_tenant.models.cityoption import CityOption
from smegurus import constants


class PostalAddressManager(models.Manager):
    def delete_all(self):
        items = PostalAddress.objects.all()
        for item in items.all():
            item.delete()


class PostalAddress(AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_postal_addresses'
        verbose_name = 'Postal Address'
        verbose_name_plural = 'Postal Addresses'

    objects = PostalAddressManager()
    country = models.ForeignKey(
        CountryOption,
        help_text=_('The country. For example, USA. You can also provide the two-letter <a href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements">ISO 3166-1 alpha-2</a> country code.'),
        null=True,
        blank=True,
        related_name="postaladdress_country_%(app_label)s_%(class)s_related",
        db_index=True,
        on_delete=models.CASCADE
    )
    postal_code = models.CharField(
        _("Postal Code"),
        max_length=127,
        help_text=_('The postal code. For example, 94043.'),
        blank=True,
        null=True,
        default='',
    )
    locality = models.CharField(
        _("Address Locality"),
        max_length=127,
        help_text=_('The locality. For example, Mountain View.'),
        blank=True,
        null=True,
        default='',
        db_index=True,
    )
    region = models.ForeignKey(
        ProvinceOption,
        help_text=_('The region. For example, CA.'),
        null=True,
        blank=True,
        related_name="postaladdress_province_%(app_label)s_%(class)s_related",
        db_index=True,
        on_delete=models.CASCADE
    )
    street_number = models.PositiveSmallIntegerField(
        _("Street Number"),
        help_text=_('The street number.'),
        blank=True,
        null=True,
        default='',
    )
    suffix = models.CharField(
        _("Suffix"),
        max_length=1,
        choices=constants.POSTALADDRESS_SUFFIX_OPTIONS,
        help_text=_('The suffix.'),
        blank=True,
        null=True,
    )
    street_name = models.CharField(
        _("Street Name"),
        max_length=127,
        help_text=_('The street name.'),
        blank=True,
        null=True,
        default='',
    )
    street_type = models.CharField(
        _("Street Type"),
        max_length=1,
        choices=constants.POSTALADDRESS_STREET_TYPE_OPTIONS,
        help_text=_('The street type.'),
        blank=True,
        null=True,
    )
    direction = models.CharField(
        _("Street Type"),
        max_length=1,
        choices=constants.POSTALADDRESS_DIRECTION_OPTIONS,
        help_text=_('The street type.'),
        blank=True,
        null=True,
    )
    suite_number = models.CharField(
        _("Suite"),
        max_length=7,
        help_text=_('The suite #.'),
        blank=True,
        null=True,
        default='',
    )
    floor_number = models.CharField(
        _("Floor"),
        max_length=7,
        help_text=_('The floor #.'),
        blank=True,
        null=True,
        default='',
    )
    buzz_number = models.CharField(
        _("Entry Code / Buzz"),
        max_length=7,
        help_text=_('The entry code.'),
        blank=True,
        null=True,
        default='',
    )
    address_line_2 = models.CharField(
        _("Address Line 2"),
        max_length=7,
        help_text=_('The address line 1.'),
        blank=True,
        null=True,
        default='',
    )
    address_line_3 = models.CharField(
        _("Address Line 3"),
        max_length=7,
        help_text=_('The address line 3.'),
        blank=True,
        null=True,
        default='',
    )

    # https://schema.org/PostalAddress

    def __str__(self):
        return str(self.name)
