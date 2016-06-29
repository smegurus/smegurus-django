from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_place import AbstractPlace


class Country(AbstractPlace):
    """
    A country.

    https://schema.org/Country
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_countries'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return str(self.name)
