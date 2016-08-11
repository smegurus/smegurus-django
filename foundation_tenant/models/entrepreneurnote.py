from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.me import TenantMe


class EntrepreneurNoteManager(models.Manager):
    def delete_all(self):
        items = EntrepreneurNote.objects.all()
        for item in items.all():
            item.delete()


class EntrepreneurNote(AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_entrepreneur_notes'
        verbose_name = _('Entrepreneur Note')
        verbose_name_plural = _('Entrepreneur Notes')

    objects = EntrepreneurNoteManager()
    me = models.ForeignKey(
        TenantMe,
        help_text=_('The entrepreneur that this Note belongs to.'),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.name)
