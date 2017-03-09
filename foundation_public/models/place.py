from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.abstract_place import AbstractPublicPlace


class PublicPlace(AbstractPublicPlace):
    """
    A place.

    https://schema.org/Place
    """
    class Meta:
        app_label = 'foundation_public'
        db_table = 'smeg_places'
        verbose_name = _('Place')
        verbose_name_plural = _('Places')

    def __str__(self):
        return str(self.name)
