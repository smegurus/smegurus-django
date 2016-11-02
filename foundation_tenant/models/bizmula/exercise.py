import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.bizmula.module import Module


class ExerciseManager(models.Manager):
    def delete_all(self):
        items = Exercise.objects.all()
        for item in items.all():
            item.delete()


class Exercise(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_exercises'
        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'

    # ------------
    #   GENERIC
    # ------------

    objects = ExerciseManager()
    module = models.ForeignKey(
        Module,
        help_text=_('The module this Exercise belongs to.'),
        blank=True,
        null=True,
        related_name="exercise_module_%(app_label)s_%(class)s_related",
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

    # ------------
    #  FUNCTIONS
    # ------------

    def __str__(self):
        return str(self.name)
