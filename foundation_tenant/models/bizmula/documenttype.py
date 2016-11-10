from django.db import models
from django.utils.translation import ugettext_lazy as _


class DocumentTypeManager(models.Manager):
    def delete_all(self):
        items = DocumentType.objects.all()
        for item in items.all():
            item.delete()


class DocumentType(models.Model):
    """
    The supported document types that our system can support.
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_document_types'
        verbose_name = _('Document Type')
        verbose_name_plural = _('Document Types')

    objects = DocumentTypeManager()
    text = models.CharField(
        _("Text"),
        max_length=127,
        help_text=_('The name of this Document Type.'),
        blank=True,
        null=True,
    )
    is_master = models.BooleanField(  # CONTROLLED BY EMPLOYEES ONLY
        _("Is Master"),
        default=False,
        help_text=_('Variable controls whether the Module this Document belongs to is the master document of the Module.'),
    )

    def __str__(self):
        return str(self.text)
