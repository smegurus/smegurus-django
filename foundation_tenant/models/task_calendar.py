from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from foundation_tenant.models.abstract_task import AbstractTask
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.logevent import SortedLogEventByCreated
from foundation_tenant.models.commentpost import SortedCommentPostByCreated
from smegurus import constants


class TaskCalendarManager(models.Manager):
    def delete_all(self):
        items = TaskCalendar.objects.all()
        for item in items.all():
            item.delete()


class TaskCalendar(AbstractTask):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_task_calendars'
        verbose_name = _('Calendar Task')
        verbose_name_plural = _('Calendar Tasks')

    objects = TaskCalendarManager()

    def __str__(self):
        return str(self.name)

#TODO: IMPLEMENT
    # def get_absolute_url(self):
    #     return reverse('tenant_TaskCalendar_details', args=[self.id])
