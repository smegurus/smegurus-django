from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.note import Note
from foundation_tenant.models.calendarevent import CalendarEvent
from foundation_tenant.models.me import TenantMe
from smegurus import constants


TASK_STATUS_OPTIONS = (
    (constants.CREATED_TASK_STATUS, _('Created')),
    (constants.PENDING_TASK_STATUS, _('Pending')),
    (constants.INCOMPLETE_TASK_STATUS, _('Incomplete')),
    (constants.COMPLETE_TASK_STATUS, _('Complete')),
)


class TaskManager(models.Manager):
    def delete_all(self):
        items = Task.objects.all()
        for item in items.all():
            item.delete()


class Task(AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    objects = TaskManager()
    note = models.ForeignKey(
        Note,
        help_text=_('The user whom this message originates from.'),
        blank=True,
        null=True,
        related_name="task_note_%(app_label)s_%(class)s_related",
        on_delete=models.SET_NULL
    )
    event = models.ForeignKey(
        CalendarEvent,
        help_text=_('The calendar event.'),
        blank=True,
        null=True,
        related_name="task_event_%(app_label)s_%(class)s_related",
        on_delete=models.SET_NULL
    )
    assigned_by = models.ForeignKey(
        TenantMe,
        help_text=_('The user whom assigned this task.'),
        blank=True,
        null=True,
        related_name="task_assigned_by_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    assignee = models.ForeignKey(
        TenantMe,
        help_text=_('The user whom is the task assigned to.'),
        blank=True,
        null=True,
        related_name="task_assignee_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    status = models.PositiveSmallIntegerField(           # CONTROLLED BY SYSTEM
        _("Status"),
        choices=TASK_STATUS_OPTIONS,
        help_text=_('The state this task.'),
        default=constants.CREATED_TASK_STATUS,
        db_index=True,
    )
    participants = models.ManyToManyField(
        TenantMe,
        help_text=_('The users participating in the conversation of this tasks.'),
        blank=True,
        related_name='task_participants_%(app_label)s_%(class)s_related',
    )

    def __str__(self):
        return str(self.name)
