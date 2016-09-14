from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.me import TenantMe


class TinyTaskManager(models.Manager):
    def delete_all(self):
        items = TinyTask.objects.all()
        for item in items.all():
            item.delete()


class TinyTask(AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_tinytasks'
        verbose_name = _('Tiny Task')
        verbose_name_plural = _('Tiny Tasks')

    objects = TinyTaskManager()
    me = models.ForeignKey(
        TenantMe,
        help_text=_('The user profile that this TinyTask belongs to.'),
        on_delete=models.CASCADE,
    )
    is_checked = models.BooleanField(
        _("Is Checked"),
        default=False,
        help_text=_('.'),
    )
    is_verified = models.BooleanField(
        _("Is Verified"),
        default=False,
        help_text=_('.'),
    )

    def __str__(self):
        return str(self.name)
