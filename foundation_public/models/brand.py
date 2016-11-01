from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.abstract_thing import AbstractPublicThing
from foundation_public.models.imageupload import PublicImageUpload


class PublicBrand(AbstractPublicThing):
    """
    A brand is a name used by an organization or business person for labeling a product, product group, or similar.

    https://schema.org/Brand
    """
    class Meta:
        app_label = 'foundation_public'
        db_table = 'smeg_brands'
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    logo = models.ForeignKey(
        PublicImageUpload,
        help_text=_('An associated logo.'),
        null=True,
        blank=True,
        related_name="brand_logo",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return str(self.name)
