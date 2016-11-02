from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.abstract_place import AbstractPlace


class PlaceManager(models.Manager):
    def delete_all(self):
        items = Place.objects.all()
        for item in items.all():
            item.delete()


class Place(AbstractPlace):
    """
    A place.

    https://schema.org/Place
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_places'
        verbose_name = 'Place'
        verbose_name_plural = 'Places'

    objects = PlaceManager()

    def __str__(self):
        return str(self.name)
