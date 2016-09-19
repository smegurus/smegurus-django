from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.abstract_task import AbstractTask
from foundation_tenant.models.fileupload import TenantFileUpload
from smegurus import constants


class TaskUploadManager(models.Manager):
    def delete_all(self):
        items = TaskUpload.objects.all()
        for item in items.all():
            item.delete()


class TaskUpload(AbstractTask):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_task_uploads'
        verbose_name = 'Upload Task'
        verbose_name_plural = 'Upload Tasks'

    objects = TaskUploadManager()
    download = models.ForeignKey(
        TenantFileUpload,
        help_text=_('The file the User must download.'),
        blank=True,
        null=True,
        related_name="upload_task_download_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    upload = models.ForeignKey(
        TenantFileUpload,
        help_text=_('The file uploaded by the User.'),
        blank=True,
        null=True,
        related_name="upload_task_upload_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.name)

    # def get_absolute_url(self):
    #     return reverse('tenant_TaskUpload_details', args=[self.id])
