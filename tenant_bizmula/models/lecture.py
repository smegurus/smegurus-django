import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class LectureManager(models.Manager):
    def delete_all(self):
        items = Lecture.objects.all()
        for item in items.all():
            item.delete()


class Lecture(models.Model):
    class Meta:
        app_label = 'tenant_bizmula'
        db_table = 'biz_lectures'
        verbose_name = 'Lecture'
        verbose_name_plural = 'Lectures'

    objects = LectureManager()
    stage_num = models.PositiveSmallIntegerField(
        _("Stage Number"),
        help_text=_('Track what stage this lecture belongs to.'),
        default=1,
        db_index=True,
    )
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

    def __str__(self):
        return str(self.title)
