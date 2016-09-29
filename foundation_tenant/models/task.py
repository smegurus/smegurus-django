from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.fileupload import TenantFileUpload
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.calendarevent import CalendarEvent
from foundation_tenant.models.logevent import SortedLogEventByCreated
from foundation_tenant.models.commentpost import SortedCommentPostByCreated
from foundation_tenant.models.inforesource import InfoResource
from smegurus import constants


class TaskManager(models.Manager):
    def delete_all(self):
        items = Task.objects.all()
        for item in items.all():
            item.delete()


class Task(AbstractThing):
    """
    This is a unified class model which will handle various task types in our
    system, including: basic, calendar, docgen, learning, webform, upload
    and resource types.
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    objects = TaskManager()
    start = models.DateTimeField(
        blank=True,
        null=True,
    )
    due = models.DateTimeField(
        blank=True,
        null=True,
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
    participants = models.ManyToManyField(                # CONTROLLED BY SYSTEM
        TenantMe,
        help_text=_('The users participating in the conversation of this tasks.'),
        blank=True,
        related_name='task_participants_%(app_label)s_%(class)s_related',
    )
    tags = models.ManyToManyField(
        Tag,
        help_text=_('The tags that this Task belongs to.'),
        blank=True,
        related_name="tasks_tags_%(app_label)s_%(class)s_related"
    )
    status = models.PositiveSmallIntegerField(            # CONTROLLED BY SYSTEM
        _("Status"),
        choices=constants.TASK_STATUS_OPTIONS,
        help_text=_('The state this task.'),
        default=constants.UNASSIGNED_TASK_STATUS,
        db_index=True,
    )
    comment_posts = models.ManyToManyField(                # CONTROLLED BY SYSTEM
        SortedCommentPostByCreated,
        help_text=_('The community posts associated with this Task.'),
        blank=True,
        related_name='task_comment_posts_%(app_label)s_%(class)s_related',
    )
    log_events = models.ManyToManyField(                  # CONTROLLED BY SYSTEM & PRIVATE
        SortedLogEventByCreated,
        help_text=_('The log events associated with this Task.'),
        blank=True,
        related_name='task_log_events_%(app_label)s_%(class)s_related',
    )
    has_review_requirement = models.BooleanField(
        _("Has Review Requirement"),
        help_text=_('Indicates whether this Task needs to be reviewed by Employees.'),
        default=False
    )
    type_of = models.PositiveSmallIntegerField(
        _("Type of Task"),
        choices=constants.TASK_TYPE_OPTIONS,
        help_text=_('The typoe of task this is.'),
        default=constants.TASK_BASIC_TYPE,
        db_index=True,
    )

    #----------------------#
    # Basic Task Fields    #
    #----------------------#
    # Nothing ...

    #----------------------#
    # Calendar Task Fields #
    #----------------------#
    calendar_event = models.ForeignKey(
        CalendarEvent,
        help_text=_('The calendar event of this Task.'),
        blank=True,
        null=True,
        related_name="task_calendar_event_%(app_label)s_%(class)s_related",
        on_delete=models.SET_NULL
    )

    #----------------------#
    # Doc Gen Task Fields  #
    #----------------------#
    # Nothing ...

    #----------------------#
    # Learning Task Fields #
    #----------------------#
    # Nothing ...

    #----------------------#
    # Web Form Task Fields #
    #----------------------#
    # Nothing ...

    #----------------------#
    # Upload Task Fields   #
    #----------------------#
    uploads = models.ManyToManyField(
        TenantFileUpload,
        help_text=_('The files uploaded by a User.'),
        blank=True,
        related_name='task_uploads_%(app_label)s_%(class)s_related',
    )

    #----------------------#
    # Resource Task Fields #
    #----------------------#
    resource = models.ForeignKey(
        InfoResource,
        help_text=_('The the InfoResource associated with this Task.'),
        blank=True,
        null=True,
        related_name="task_resource_%(app_label)s_%(class)s_related",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return str(self.name)
