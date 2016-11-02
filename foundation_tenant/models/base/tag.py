from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.abstract_thing import AbstractThing


class TagManager(models.Manager):
    def delete_all(self):
        items = Tag.objects.all()
        for item in items.all():
            item.delete()


class Tag(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_tags'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    objects = TagManager()
    name = models.CharField(
        _("Name"),
        max_length=127,
        help_text=_('The name of the Tag item.'),
        unique=True,
    )
    is_program = models.BooleanField(
        _("Is program"),
        help_text=_('Indicates if this Tag is to be used for programs.'),
        default=False,
        blank=True,
    )

    def __str__(self):
        return str(self.name)
