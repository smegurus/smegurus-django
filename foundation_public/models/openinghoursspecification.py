from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.abstract_thing import AbstractPublicThing


class PublicOpeningHoursSpecification(AbstractPublicThing):
    """
    A structured value providing information about the opening hours of a place or a certain service inside a place.

    https://schema.org/OpeningHoursSpecification
    """
    class Meta:
        app_label = 'foundation_public'
        db_table = 'smeg_opening_hours_specifications'
        verbose_name = _('Opening Hours Specification')
        verbose_name_plural = _('Opening Hours Specifications')

    closes = models.CharField(
        _("Closes"),
        max_length=5,
        help_text=_('The closing hour of the place or service on the given day(s) of the week.'),
        blank=True,
        null=True,
    )
    day_of_week = models.CharField(
        _("Day Of Week"),
        max_length=2,
        help_text=_('The day of the week for which these opening hours are valid.'),
        blank=True,
        null=True,
    )
    opens = models.CharField(
        _("Opens"),
        max_length=5,
        help_text=_('The opening hour of the place or service on the given day(s) of the week.'),
        blank=True,
        null=True,
    )
    valid_from = models.DateField(
        _("Valid From"),
        help_text=_('The date when the item becomes valid.'),
        blank=True,
        null=True
    )
    valid_through = models.DateField(
        _("Valid Through"),
        help_text=_('The end of the validity of offer, price specification, or opening hours data.'),
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.name)
