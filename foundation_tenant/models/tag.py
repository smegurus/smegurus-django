from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing


class Tag(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_tags'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_('The name of the item.'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)
