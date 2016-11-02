from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.abstract_thing import AbstractThing
from foundation_tenant.models.bizmula.workspace import Workspace


class DocumentManager(models.Manager):
    def delete_all(self):
        items = Document.objects.all()
        for item in items.all():
            item.delete()


class Document(AbstractThing):
    """
    A Document is a name used by an organization or business person for labeling a product, product group, or similar.

    https://schema.org/Document
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_documents'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    objects = DocumentManager()
    workspace = models.ForeignKey(
        Workspace,
        help_text=_('The Workspace this Document belongs to.'),
        blank=True,
        null=True,
        related_name="document_workspace_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    is_ready = models.BooleanField(
        _("Is Ready"),
        help_text=_('Indicates whether this document has been generated and ready for consumption or not.'),
        default=False,
        blank=True,
    )

    def __str__(self):
        return str(self.name)
