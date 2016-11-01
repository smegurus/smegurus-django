import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from tenant_bizmula.models.lecture import Lecture


class SlideManager(models.Manager):
    def delete_all(self):
        items = Slide.objects.all()
        for item in items.all():
            item.delete()


class Slide(models.Model):
    class Meta:
        app_label = 'tenant_bizmula'
        db_table = 'biz_slides'
        verbose_name = 'Slide'
        verbose_name_plural = 'Slide'

    objects = SlideManager()
    lecture = models.ForeignKey(
        Lecture,
        help_text=_('The lecture this slide belongs to.'),
        blank=True,
        null=True,
        related_name="slide_lecture_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    page_num = models.PositiveSmallIntegerField(
        _("Page Number"),
        help_text=_('The page number in the slides for the lecture.'),
        default=1,
        db_index=True,
    )
    intro_title = models.CharField(
        _("Introduction Title"),
        max_length=255,
        help_text=_('The name of the City.'),
        blank=True,
        null=True,
    )
    intro_description = models.TextField(
        _("Introduction Description"),
        help_text=_('A short description of the item.'),
        blank=True,
        null=True,
        default='',
    )
    video = models.FileField(
        _("File"),
        help_text=_('An file of the upload.'),
        upload_to='upload',
        null=True,
        blank=True
    )
    outro_title = models.CharField(
        _("Outro Title"),
        max_length=255,
        help_text=_('The name of the City.'),
        blank=True,
        null=True,
    )
    outro_description = models.TextField(
        _("Outro Description"),
        help_text=_('A short description of the item.'),
        blank=True,
        null=True,
        default='',
    )

    def __str__(self):
        return str(self.name)
