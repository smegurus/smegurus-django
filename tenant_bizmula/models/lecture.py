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

    # ------------
    #   GENERIC
    # ------------

    objects = LectureManager()

    # ------------
    #  NAVIGATION
    # ------------

    stage_num = models.PositiveSmallIntegerField(
        _("Stage Number"),
        help_text=_('Track what stage this lecture belongs to.'),
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
