from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.imageupload import TenantImageUpload


class Brand(AbstractThing):
    """
    A brand is a name used by an organization or business person for labeling a product, product group, or similar.

    https://schema.org/Brand
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_brands'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    logo = models.ForeignKey(
        TenantImageUpload,
        help_text=_('An associated logo.'),
        null=True,
        blank=True,
        related_name="brand_logo"
    )

    def __str__(self):
        return str(self.name)
