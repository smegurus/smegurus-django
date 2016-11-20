from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.bizmula.documenttype import DocumentType


class QuestionManager(models.Manager):
    def delete_all(self):
        items = Question.objects.all()
        for item in items.all():
            item.delete()


class Question(models.Model):
    """
    The supported document types that our system can support.
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_questions'
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ("number",)

    objects = QuestionManager()
    document_type = models.ForeignKey(
        DocumentType,
        help_text=_('The document type this question belongs to.'),
        blank=True,
        null=True,
        related_name="question_document_type%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    number = models.PositiveSmallIntegerField(
        _("Number"),
        help_text=_('The number to display for this question.'),
        default=0,
        blank=True,
        null=True,
    )
    title = models.CharField(
        _("Title"),
        max_length=255,
        help_text=_('The title of this question.'),
        blank=True,
        null=True,
    )
    help = models.CharField(
        _("Help"),
        max_length=511,
        help_text=_('The title of this question.'),
        blank=True,
        null=True,
    )
    options = JSONField( # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#jsonfield
        _("Options"),
        help_text=_('The options to populate the question with.'),
        blank=True,
        default="[]"
    )
    content = JSONField( # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#jsonfield
        _("Content"),
        help_text=_('The content to populate the question with.'),
        blank=True,
        default="{}"
    )
    template_id = models.PositiveSmallIntegerField(
        _("Template ID"),
        help_text=_('The template ID to load up for the view.'),
        default=0,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.title)
