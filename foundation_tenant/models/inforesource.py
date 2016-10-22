from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.imageupload import TenantImageUpload
from foundation_tenant.models.fileupload import TenantFileUpload
from foundation_tenant.models.inforesourcecategory import InfoResourceCategory
from smegurus import constants


class InfoResourceManager(models.Manager):
    def delete_all(self):
        items = InfoResource.objects.all()
        for item in items.all():
            item.delete()


class InfoResource(AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_info_resources'
        verbose_name = 'Information Resource'
        verbose_name_plural = 'Information Resources'

    objects = InfoResourceManager()
    category = models.ForeignKey(
        InfoResourceCategory,
        help_text=_('The category.'),
        null=True,
        blank=True,
        related_name="info_resource_category",
        on_delete=models.SET_NULL
    )
    type_of = models.PositiveSmallIntegerField(
        _("Type of resource"),
        choices=constants.INFO_RESOURCE_TYPE_OPTIONS,
        help_text=_('The type of resource this is.'),
        default=constants.INFO_RESOURCE_INTERAL_URL_TYPE
    )
    upload = models.ForeignKey(
        TenantFileUpload,
        help_text=_('The uploaded file.'),
        null=True,
        blank=True,
        related_name="info_resource_uploaded_file",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return str(self.name)
