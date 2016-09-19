from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from foundation_tenant.models.abstract_task import AbstractTask
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.logevent import SortedLogEventByCreated
from foundation_tenant.models.commentpost import SortedCommentPostByCreated
from smegurus import constants


class BasicTaskManager(models.Manager):
    def delete_all(self):
        items = BasicTask.objects.all()
        for item in items.all():
            item.delete()


class BasicTask(AbstractTask):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_basic_tasks'
        verbose_name = _('Basic Task')
        verbose_name_plural = _('Basic Tasks')

    objects = BasicTaskManager()

    def __str__(self):
        return str(self.name)

#TODO: IMPLEMENT
    # def get_absolute_url(self):
    #     return reverse('tenant_basicTask_details', args=[self.id])
