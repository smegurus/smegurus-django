from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.abstract_place import AbstractPublicPlace


class PublicCountry(AbstractPublicPlace):
    """
    A country.

    https://schema.org/Country
    """
    class Meta:
        app_label = 'foundation_public'
        db_table = 'smeg_countries'
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return str(self.name)
