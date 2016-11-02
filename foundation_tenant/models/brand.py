from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.base.imageupload import TenantImageUpload


class BrandManager(models.Manager):
    def delete_all(self):
        items = Brand.objects.all()
        for item in items.all():
            item.delete()


class Brand(AbstractThing):
    """
    A brand is a name used by an organization or business person for labeling a product, product group, or similar.

    https://schema.org/Brand
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_brands'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    objects = BrandManager()
    logo = models.ForeignKey(
        TenantImageUpload,
        help_text=_('An associated logo.'),
        null=True,
        blank=True,
        related_name="brand_logo",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return str(self.name)
