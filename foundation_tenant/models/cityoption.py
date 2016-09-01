import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.countryoption import CountryOption
from foundation_tenant.models.provinceoption import ProvinceOption


class CityOptionManager(models.Manager):
    def delete_all(self):
        items = CityOption.objects.all()
        for item in items.all():
            item.delete()


class CityOption(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_city_options'
        verbose_name = 'City Option'
        verbose_name_plural = 'City Options'

    objects = CityOptionManager()
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_('The name of the City.'),
        blank=True,
        null=True,
    )
    country = models.ForeignKey(
        CountryOption,
        help_text=_('The country this City belongs to.'),
        null=True,
        blank=True,
        related_name="city_country_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    province = models.ForeignKey(
        ProvinceOption,
        help_text=_('The Province this City belongs to.'),
        null=True,
        blank=True,
        related_name="city_province_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    # NOTE: A complete list of time zones can be found here: http://stackoverflow.com/q/13866926
    time_zone = models.CharField(
        _("Timezone"),
        max_length=255,
        help_text=_('The timezone this city belongs to.'),
        blank=True,
        null=True,
        default='America/Toronto',
    )

    def __str__(self):
        return str(self.name)
