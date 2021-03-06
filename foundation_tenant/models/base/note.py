from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.abstract_bigpk import AbstractBigPk
from foundation_tenant.models.base.abstract_thing import AbstractThing
from foundation_tenant.models.base.me import Me


class NoteManager(models.Manager):
    def delete_all(self):
        items = Note.objects.all()
        for item in items.all():
            item.delete()


class Note(AbstractThing, AbstractBigPk):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_notes'
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')

    objects = NoteManager()
    me = models.ForeignKey(
        Me,
        help_text=_('The user profile that this Note belongs to.'),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.name)
