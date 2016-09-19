from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.abstract_task import AbstractTask
from smegurus import constants


class LearningTaskManager(models.Manager):
    def delete_all(self):
        items = LearningTask.objects.all()
        for item in items.all():
            item.delete()


class LearningTask(AbstractTask):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_learning_tasks'
        verbose_name = 'Learning Task'
        verbose_name_plural = 'Learning Tasks'

    objects = LearningTaskManager()

    #TODO: IMPLEMENT

    def __str__(self):
        return str(self.name)

    # def get_absolute_url(self):
    #     return reverse('tenant_LearningTask_details', args=[self.id])
