from django.db import models
from django.utils.translation import ugettext_lazy as _


class IdentifyOptionManager(models.Manager):
    def delete_all(self):
        items = IdentifyOption.objects.all()
        for item in items.all():
            item.delete()


class IdentifyOption(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        ordering = ('order_number',)
        db_table = 'smeg_identify_options'
        verbose_name = _('Identify Option')
        verbose_name_plural = _('Identify Options')

    objects = IdentifyOptionManager()
    order_number = models.PositiveSmallIntegerField(
        _("Order Number"),
        help_text=_('The order to display this model as.'),
        default=0,
    )
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_('The name of the identity.'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)
