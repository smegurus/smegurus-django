from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.abstract_thing import AbstractPublicThing
from foundation_public.models.imageupload import PublicImageUpload
from foundation_public.models.postaladdress import PublicPostalAddress
from foundation_public.models.geocoordinate import PublicGeoCoordinate
from foundation_public.models.openinghoursspecification import PublicOpeningHoursSpecification


class AbstractPublicPlace(AbstractPublicThing):
    """
    Entities that have a somewhat fixed, physical extension.

    https://schema.org/Place
    """
    class Meta:
        abstract = True

    # additionalProperty
    address = models.ForeignKey(
        PublicPostalAddress,
        help_text=_('Physical address of the item.'),
        null=True,
        blank=True,
        related_name="place_address_%(app_label)s_%(class)s_related",
        on_delete=models.SET_NULL
    )
    # aggregateRating
    # branchCode
    # containedInPlace
    # containsPlace
    # event
    fax_number = models.CharField(
        _("Fax Number"),
        max_length=31,
        help_text=_('The fax number.'),
        blank=True,
        null=True,
    )
    geo = models.ForeignKey(
        PublicGeoCoordinate,
        help_text=_('The geo coordinates of the place.'),
        null=True,
        blank=True,
        related_name="place_geo_%(app_label)s_%(class)s_related",
        on_delete=models.SET_NULL
    )
    global_location_number = models.CharField(
        _("Global Location Number"),
        max_length=255,
        help_text=_('The <a href="http://www.gs1.org/gln">Global Location Number</a> (GLN, sometimes also referred to as International Location Number or ILN) of the respective organization, person, or place. The GLN is a 13-digit number used to identify parties and physical locations.'),
        blank=True,
        null=True,
    )
    has_map = models.URLField(
        _("Has Map"),
        help_text=_('A URL to a map of the place.'),
        null=True,
        blank=True
    )
    isic_v4 = models.CharField(
        _("ISIC V4"),
        max_length=255,
        help_text=_('The International Standard of Industrial Classification of All Economic Activities (ISIC), Revision 4 code for a particular organization, business person, or place.'),
        blank=True,
        null=True,
    )
    logo = models.ForeignKey(
        PublicImageUpload,
        help_text=_('An associated logo.'),
        null=True,
        blank=True,
        related_name="place_logo_%(app_label)s_%(class)s_related",
        on_delete=models.SET_NULL
    )
    opening_hours_specification = models.ManyToManyField(
        PublicOpeningHoursSpecification,
        help_text=_('The hours during which this service or contact is available.'),
        blank=True,
        related_name='place_hours_available_%(app_label)s_%(class)s_related',
    )
    photo = models.ForeignKey(
        PublicImageUpload,
        help_text=_('A photograph of this place.'),
        null=True,
        blank=True,
        related_name="place_photo_%(app_label)s_%(class)s_related",
        on_delete=models.SET_NULL
    )
    # review
    telephone = models.CharField(
        _("Telephone"),
        max_length=31,
        help_text=_('The telephone number.'),
        blank=True,
        null=True,
    )
