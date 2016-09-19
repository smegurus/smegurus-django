from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from foundation_tenant.models.abstract_task import AbstractTask
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.logevent import SortedLogEventByCreated
from foundation_tenant.models.commentpost import SortedCommentPostByCreated
from smegurus import constants


class TaskBasicManager(models.Manager):
    def delete_all(self):
        items = TaskBasic.objects.all()
        for item in items.all():
            item.delete()


class TaskBasic(AbstractTask):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_task_basics'
        verbose_name = _('Basic Task')
        verbose_name_plural = _('Basic Tasks')

    objects = TaskBasicManager()

    def __str__(self):
        return str(self.name)

#TODO: IMPLEMENT
    # def get_absolute_url(self):
    #     return reverse('tenant_TaskBasic_details', args=[self.id])
