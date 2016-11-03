from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.bizmula.question import Question


class QuestionOptionManager(models.Manager):
    def delete_all(self):
        items = QuestionOption.objects.all()
        for item in items.all():
            item.delete()


class QuestionOption(models.Model):
    """
    The supported document types that our system can support.
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_question_options'
        verbose_name = _('Question Option')
        verbose_name_plural = _('Question Options')
        ordering = ("order_num",)

    objects = QuestionOptionManager()
    question = models.ForeignKey(
        Question,
        help_text=_('The question this option belongs to.'),
        blank=True,
        null=True,
        related_name="question_option_question_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    alternate_id = models.PositiveSmallIntegerField(
        _("Alternate ID"),
        help_text=_('Alternative ID to use.'),
        default=0,
        blank=True,
        null=True,
    )
    order_num = models.PositiveSmallIntegerField(
        _("Order Number"),
        help_text=_('The order number to sort option by.'),
        default=0,
        blank=True,
        null=True,
    )
    text = models.CharField(
        _("Text"),
        max_length=63,
        help_text=_('The title of this QuestionOption.'),
        blank=True,
        null=True,
    )
    value = models.CharField(
        _("Value"),
        max_length=63,
        help_text=_('The title of this QuestionOption.'),
        blank=True,
        null=True,
    )
    help = models.CharField(
        _("Help"),
        max_length=255,
        help_text=_('The title of this question.'),
        blank=True,
        null=True,
    )
    parent = models.ForeignKey(
        'self',
        help_text=_('The parent option this option belongs to.'),
        blank=True,
        null=True,
        related_name="question_option_parent_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )


    def __str__(self):
        return str(self.title)
