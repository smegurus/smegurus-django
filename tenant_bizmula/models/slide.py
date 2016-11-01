import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from tenant_bizmula.models.module import Module


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
        verbose_name_plural = 'Slides'
        ordering = ('page_num',)

    # ------------
    #   GENERIC
    # ------------

    objects = SlideManager()
    module = models.ForeignKey(
        Module,
        help_text=_('The module this slide belongs to.'),
        blank=True,
        null=True,
        related_name="slide_module_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )

    # ------------
    #  NAVIGATION
    # ------------

    previous_slide_id = models.PositiveSmallIntegerField(
        _("Previous Slide ID"),
        help_text=_('The previous slide ID.'),
        default=0,
        blank=True,
        null=True,
    )
    next_slide_id = models.PositiveSmallIntegerField(
        _("Next Slide ID"),
        help_text=_('The next slide ID.'),
        default=0,
        blank=True,
        null=True,
    )
    next_exercise_id = models.PositiveSmallIntegerField(
        _("Exercise ID"),
        help_text=_('The exercise ID to load up next.'),
        default=0,
        blank=True,
        null=True,
    )
    page_num = models.PositiveSmallIntegerField(
        _("Page Number"),
        help_text=_('The page number in the slides for the module.'),
        default=1,
        db_index=True,
    )

    # ------------
    #   CONTENT
    # ------------

    title = models.CharField(
        _("Introduction Title"),
        max_length=255,
        help_text=_('The name of the City.'),
        blank=True,
        null=True,
    )
    description = models.TextField(
        _("Introduction Description"),
        help_text=_('A short description of the item.'),
        blank=True,
        null=True,
        default='',
    )
    video = models.FileField(
        _("Video"),
        help_text=_('An file of the upload.'),
        upload_to='upload',
        null=True,
        blank=True
    )

    # ------------
    #  FUNCTIONS
    # ------------

    def __str__(self):
        return str(self.name)
