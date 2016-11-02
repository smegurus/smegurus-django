from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.abstract_thing import AbstractThing
from foundation_tenant.models.base.imageupload import TenantImageUpload
from foundation_tenant.models.base.fileupload import TenantFileUpload
from foundation_tenant.models.base.inforesourcecategory import InfoResourceCategory
from foundation_tenant.models.base.tag import Tag
from smegurus import constants


class InfoResourceManager(models.Manager):
    def delete_all(self):
        items = InfoResource.objects.all()
        for item in items.all():
            item.delete()


class InfoResource(AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_info_resources'
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
    is_stock = models.BooleanField(
        _("Is this resource a stock resource"),
        default=False,
        help_text=_('Variable controls whether this resource was created by the system and cannot be deleted.'),
    )
    is_for_staff = models.BooleanField(
        _("Is this resource available to the staff"),
        default=False,
        help_text=_('Variable controls whether staff will see this resource.'),
    )
    is_for_entrepreneur = models.BooleanField(
        _("Is this resource available to the entrepreneur"),
        default=False,
        help_text=_('Variable controls whether entrepreneurs will see this resource.'),
    )
    stage_num = models.PositiveSmallIntegerField(
        _("Stage Number"),
        help_text=_('Track what stage this resource is accessible for the entrepreneur.'),
        default=1,
        db_index=True,
    )
    uploads = models.ManyToManyField(
        TenantFileUpload,
        help_text=_('The files uploaded by a User.'),
        blank=True,
        related_name='info_resources_uploads_%(app_label)s_%(class)s_related',
    )
    tags = models.ManyToManyField(
        Tag,
        help_text=_('The tags that this User belongs to.'),
        blank=True,
        related_name="info_resources_tags_%(app_label)s_%(class)s_related"
    )

    def __str__(self):
        return str(self.name)
