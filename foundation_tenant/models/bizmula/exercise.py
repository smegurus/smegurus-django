from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.bizmula.module import Module
from foundation_tenant.models.bizmula.documenttype import DocumentType


class ExerciseManager(models.Manager):
    def delete_all(self):
        items = Exercise.objects.all()
        for item in items.all():
            item.delete()


class Exercise(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_exercises'
        verbose_name = _('Exercise')
        verbose_name_plural = _('Exercises')

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
    document_type = models.ForeignKey(
        DocumentType,
        help_text=_('The document type that this Exercises questions belongs to.'),
        blank=True,
        null=True,
        related_name="exercise_document_type_%(app_label)s_%(class)s_related",
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
        max_length=127,
        help_text=_('The name of this exercise.'),
        blank=True,
        null=True,
    )
    question_ids = ArrayField(
        models.PositiveSmallIntegerField(),
        help_text=_('The question IDs that belong to this exercise.'),
        blank=True,
        null=True,
    )

    # ------------
    #  FUNCTIONS
    # ------------

    def __str__(self):
        return str(self.title)

    def next_question_id(self, start_question_id):
        """
        Function will iterate through the question IDs and find the next
        question ID from the inputted param.
        """
        for question_id in self.question_ids:
            if question_id > start_question_id:
                return question_id
        return start_question_id

    def previous_question_id(self, start_question_id):
        """
        Function will iterate through the question IDs and find the previous
        question ID from the inputted param.
        """
        for question_id in self.question_ids:
            if question_id < start_question_id:
                return question_id
        return start_question_id

    def last_question_id(self):
        """
        Function will iterate through the question IDs and find the last
        question ID.
        """
        last_question_id = 0
        for question_id in self.question_ids:
            if question_id >= last_question_id:
                last_question_id = question_id
        return last_question_id
