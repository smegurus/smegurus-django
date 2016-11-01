from django.db import models
from django.utils.translation import ugettext_lazy as _


class CountryOptionManager(models.Manager):
    def delete_all(self):
        items = CountryOption.objects.all()
        for item in items.all():
            item.delete()


class CountryOption(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_country_options'
        verbose_name = 'Country Option'
        verbose_name_plural = 'Country Options'

    objects = CountryOptionManager()
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_('The name of the Country.'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)
