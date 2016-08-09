from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing


class PostalAddressManager(models.Manager):
    def delete_all(self):
        items = PostalAddress.objects.all()
        for item in items.all():
            item.delete()


class PostalAddress(AbstractThing):
    """
    The mailing address.

    https://schema.org/PostalAddress
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_postal_addresses'
        verbose_name = 'Postal Address'
        verbose_name_plural = 'Postal Addresses'

    objects = PostalAddressManager()
    address_country = models.CharField(
        _("Address Country"),
        max_length=127,
        help_text=_('The country. For example, USA. You can also provide the two-letter <a href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements">ISO 3166-1 alpha-2</a> country code.'),
        blank=True,
        null=True,
        default='',
    )
    address_locality = models.CharField(
        _("Address Locality"),
        max_length=127,
        help_text=_('The locality. For example, Mountain View.'),
        blank=True,
        null=True,
        default='',
    )
    address_region = models.CharField(
        _("Address Region"),
        max_length=127,
        help_text=_('The region. For example, CA.'),
        blank=True,
        null=True,
        default='',
    )
    post_office_box_number = models.CharField(
        _("Post Office Box Number"),
        max_length=127,
        help_text=_('The post office box number for PO box addresses.'),
        blank=True,
        null=True,
        default='',
    )
    postal_code = models.CharField(
        _("Postal Code"),
        max_length=127,
        help_text=_('The postal code. For example, 94043.'),
        blank=True,
        null=True,
        default='',
    )
    street_address = models.CharField(
        _("Street Address"),
        max_length=255,
        help_text=_('The street address. For example, 1600 Amphitheatre Pkwy.'),
        blank=True,
        null=True,
        default='',
    )

    def __str__(self):
        return str(self.name)
