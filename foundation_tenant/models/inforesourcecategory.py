from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.imageupload import TenantImageUpload
from foundation_tenant.models.fileupload import TenantFileUpload
from smegurus import constants


class InfoResourceCategoryManager(models.Manager):
    def delete_all(self):
        items = InfoResourceCategory.objects.all()
        for item in items.all():
            item.delete()


class InfoResourceCategory(AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_info_resource_categories'
        verbose_name = 'Information Resource Category'
        verbose_name_plural = 'Information Resources Category'

    objects = InfoResourceCategoryManager()
    order_num = models.PositiveSmallIntegerField(
        _("Order Number"),
        help_text=_('The order this category is to be ordered by.'),
        default=0
    )
    icon = models.CharField(
        _("Icon"),
        max_length=31,
        help_text=_('The icon of this category.'),
        blank=True,
        null=True,
    )
    colour = models.CharField(
        _("Colour"),
        max_length=15,
        help_text=_('The colour of this category.'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)
