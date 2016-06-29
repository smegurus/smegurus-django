from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing


class GeoCoordinate(AbstractThing):
    """
    The geographic coordinates of a place or event.

    https://schema.org/GeoCoordinates
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_geocoordinates'
        verbose_name = 'GeoCoordinate'
        verbose_name_plural = 'GeoCoordinates'

    address = models.CharField(
        _("Address"),
        max_length=255,
        help_text=_('Physical address of the item.'),
        blank=True,
        null=True,
    )
    address_country = models.CharField(
        _("Address Country"),
        max_length=255,
        help_text=_('The country. For example, USA. You can also provide the two-letter <a href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements">ISO 3166-1 alpha-2</a> country code.'),
        blank=True,
        null=True,
    )
    elevation = models.FloatField(
        _("Elevation"),
        help_text=_('The elevation of a location (<a href="https://en.wikipedia.org/wiki/World_Geodetic_System">WGS 84</a>).'),
        blank=True,
        default=0.00,
    )
    latitude = models.FloatField(
        _("Latitude"),
        help_text=_('The latitude of a location. For example 37.42242 (<a href="https://en.wikipedia.org/wiki/World_Geodetic_System">WGS 84</a>).'),
        blank=True,
        default=0.00,
    )
    longitude = models.FloatField(
        _("Longitude"),
        help_text=_('The longitude of a location. For example -122.08585 (<a href="https://en.wikipedia.org/wiki/World_Geodetic_System">WGS 84</a>).'),
        blank=True,
        default=0.00,
    )
    postal_code = models.CharField(
        _("Postal Code"),
        max_length=127,
        help_text=_('The postal code. For example, 94043.'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)
