from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.abstract_thing import AbstractPublicThing
from foundation_public.models.language import PublicLanguage
from foundation_public.models.openinghoursspecification import PublicOpeningHoursSpecification


class PublicContactPoint(AbstractPublicThing):
    """
    A contact point—for example, a Customer Complaints department.

    https://schema.org/ContactPoint
    """
    class Meta:
        app_label = 'foundation_public'
        db_table = 'biz_contact_points'
        verbose_name = 'Contact Point'
        verbose_name_plural = 'Contact Points'

    area_served = models.CharField(
        _("Area Served"),
        max_length=127,
        help_text=_('The geographic area where a service or offered item is provided.'),
        blank=True,
        null=True,
    )
    available_language = models.ForeignKey(
        PublicLanguage,
        help_text=_('A language someone may use with the item.'),
        null=True,
        blank=True,
        related_name="public_contact_point_available_language_%(app_label)s_%(class)s_related",
        on_delete=models.SET_NULL
    )
    contact_type = models.CharField(
        _("Contact Type"),
        max_length=127,
        help_text=_('A person or organization can have different contact points, for different purposes. For example, a sales contact point, a PR contact point and so on. This property is used to specify the kind of contact point.'),
        blank=True,
        null=True,
    )
    email = models.EmailField(
        _("Email"),
        help_text=_('Email address.'),
        null=True,
        blank=True
    )
    fax_number = models.CharField(
        _("Fax Number"),
        max_length=31,
        help_text=_('The fax number.'),
        blank=True,
        null=True,
    )
    hours_available = models.ManyToManyField(
        PublicOpeningHoursSpecification,
        help_text=_('The hours during which this service or contact is available.'),
        blank=True,
        related_name="public_contact_point_hours_available_%(app_label)s_%(class)s_related"
    )
    product_supported = models.CharField(
        _("Product Supported"),
        max_length=31,
        help_text=_('The product or service this support contact point is related to (such as product support for a particular product line). This can be a specific product or product line (e.g. "iPhone") or a general category of products or services (e.g. "smartphones").'),
        blank=True,
        null=True,
    )
    telephone = models.CharField(
        _("Telephone"),
        max_length=31,
        help_text=_('The telephone number.'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)
