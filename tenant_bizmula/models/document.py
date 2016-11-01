from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.imageupload import TenantImageUpload


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
        app_label = 'tenant_bizmula'
        db_table = 'biz_documents'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    objects = DocumentManager()

    def __str__(self):
        return str(self.name)
