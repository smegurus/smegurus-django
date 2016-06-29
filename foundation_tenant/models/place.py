from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_place import AbstractPlace


class Place(AbstractPlace):
    """
    A place.

    https://schema.org/Place
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_places'
        verbose_name = 'Place'
        verbose_name_plural = 'Places'

    def __str__(self):
        return str(self.name)
