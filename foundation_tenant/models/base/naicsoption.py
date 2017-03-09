import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.countryoption import CountryOption


class NAICSOptionManager(models.Manager):
    def delete_all(self):
        items = NAICSOption.objects.all()
        for item in items.all():
            item.delete()


class NAICSOption(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        ordering = ['seq_num',]
        db_table = 'smeg_naics_options'
        verbose_name = _('NAICS Option')
        verbose_name_plural = _('NAICS Options')

    objects = NAICSOptionManager()
    seq_num = models.PositiveSmallIntegerField(
        _("Sequence Number"),
        help_text=_('The order number this NAICS option is ordered by.'),
        default=0,
    )
    name = models.CharField(
        _("Name"),
        max_length=127,
        help_text=_('The name of the NAICS Option.'),
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        'self',
        help_text=_('The NAICS parent that this object belongs to.'),
        null=True,
        blank=True,
        related_name="naics_option_country_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    year = models.PositiveSmallIntegerField(
        _("Year"),
        help_text=_('The year this NAICS option was issued.'),
        default=2012,
    )

    def __str__(self):
        return str(self.name)
