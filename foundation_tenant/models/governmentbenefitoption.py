from django.db import models
from django.utils.translation import ugettext_lazy as _


class GovernmentBenefitOptionManager(models.Manager):
    def delete_all(self):
        items = GovernmentBenefitOption.objects.all()
        for item in items.all():
            item.delete()


class GovernmentBenefitOption(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        ordering = ('order_number')
        db_table = 'biz_government_benefit_options'
        verbose_name = 'Government Benefit Option'
        verbose_name_plural = 'Government Benefit Options'

    objects = GovernmentBenefitOptionManager()
    order_number = models.PositiveSmallIntegerField(
        _("Order Number"),
        help_text=_('The order to display this model as.'),
        default=0,
    )
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_('The name of the benefit.'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)
