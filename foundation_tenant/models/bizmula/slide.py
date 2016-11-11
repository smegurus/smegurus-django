import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.bizmula.module import Module


class SlideManager(models.Manager):
    def delete_all(self):
        items = Slide.objects.all()
        for item in items.all():
            item.delete()


class Slide(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_slides'
        verbose_name = _('Slide')
        verbose_name_plural = _('Slides')

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
    #   CONTENT
    # ------------

    title = models.CharField(
        _("Introduction Title"),
        max_length=127,
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
    video_url = models.URLField(
        _("Video URL"),
        help_text=_('The URL of our video for this slide.'),
        null=True,
        blank=True
    )

    # ------------
    #  FUNCTIONS
    # ------------

    def __str__(self):
        return str(self.title)
