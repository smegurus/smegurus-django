from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.bizmula.workspace import Workspace
from foundation_tenant.models.bizmula.document import Document
from foundation_tenant.models.bizmula.question import Question


class QuestionAnswerManager(models.Manager):
    def delete_all(self):
        items = QuestionAnswer.objects.all()
        for item in items.all():
            item.delete()


class QuestionAnswer(models.Model):
    """
    The supported document types that our system can support.
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_question_answers'
        verbose_name = _('Question Answer')
        verbose_name_plural = _('Question Answers')

    objects = QuestionAnswerManager()
    workspace = models.ForeignKey(
        Workspace,
        help_text=_('The workspace this answer belongs to.'),
        blank=True,
        null=True,
        related_name="question_answer_workspace_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    document = models.ForeignKey(
        Document,
        help_text=_('The document this answer belongs to.'),
        blank=True,
        null=True,
        related_name="question_answer_document_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        help_text=_('The question this option belongs to.'),
        blank=True,
        null=True,
        related_name="question_answer_question_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    content = JSONField( # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#jsonfield
        _("content"),
        help_text=_('The content to populate the QuestionAnswer with.'),
        blank=True,
        default={}
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.question)
