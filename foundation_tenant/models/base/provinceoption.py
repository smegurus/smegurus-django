import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.countryoption import CountryOption


class ProvinceOptionManager(models.Manager):
    def delete_all(self):
        items = ProvinceOption.objects.all()
        for item in items.all():
            item.delete()


class ProvinceOption(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_province_options'
        verbose_name = _('Province Option')
        verbose_name_plural = _('Province Options')

    objects = ProvinceOptionManager()
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_('The name of the Province Option.'),
        blank=True,
        null=True,
    )
    country = models.ForeignKey(
        CountryOption,
        help_text=_('The country this Province/state belongs to.'),
        null=True,
        blank=True,
        related_name="province_option_country_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.name)
