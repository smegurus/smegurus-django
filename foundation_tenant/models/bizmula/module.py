import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class ModuleManager(models.Manager):
    def delete_all(self):
        items = Module.objects.all()
        for item in items.all():
            item.delete()


class Module(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_modules'
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'

    # ------------
    #   GENERIC
    # ------------

    objects = ModuleManager()

    # ------------
    #  NAVIGATION
    # ------------

    stage_num = models.PositiveSmallIntegerField(
        _("Stage Number"),
        help_text=_('Track what stage this Module belongs to.'),
        default=1,
        db_index=True,
    )
    start_slide_id = models.PositiveSmallIntegerField(
        _("Start Slide ID"),
        help_text=_('The start slide ID to begin with.'),
        default=0,
        blank=True,
        null=True,
    )

    # ------------
    #  CONTENT
    # ------------

    title = models.CharField(
        _("Title"),
        max_length=127,
        help_text=_('The name of the City.'),
        blank=True,
        null=True,
    )
    description = models.TextField(
        _("Description"),
        help_text=_('A short description of the item.'),
        blank=True,
        null=True,
        default='',
    )
    icon = models.CharField(
        _("Icon"),
        max_length=31,
        help_text=_('The name of the City.'),
        blank=True,
        null=True,
    )
    colour = models.CharField(
        _("Colour"),
        max_length=31,
        help_text=_('The name of the City.'),
        blank=True,
        null=True,
    )

    # ------------
    #  FUNCTIONS
    # ------------

    def __str__(self):
        return str(self.title)
