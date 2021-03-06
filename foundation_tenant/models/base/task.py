from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from foundation_tenant.models.base.abstract_thing import AbstractThing
from foundation_tenant.models.base.abstract_bigpk import AbstractBigPk
from foundation_tenant.models.base.fileupload import FileUpload
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.me import Me
from foundation_tenant.models.base.calendarevent import CalendarEvent
from foundation_tenant.models.base.logevent import SortedLogEventByCreated
from foundation_tenant.models.base.commentpost import SortedCommentPostByCreated
from foundation_tenant.models.base.inforesource import InfoResource
from smegurus import constants


class TaskManager(models.Manager):
    def delete_all(self):
        items = Task.objects.all()
        for item in items.all():
            item.delete()


class Task(AbstractThing, AbstractBigPk):
    """
    This is a unified class model which will handle various task types in our
    system, including: basic, calendar, docgen, learning, webform, upload
    and resource types.
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_tasks'
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    objects = TaskManager()
    status = models.PositiveSmallIntegerField(            # CONTROLLED BY SYSTEM
        _("Status"),
        choices=constants.TASK_STATUS_OPTIONS,
        help_text=_('The state this task.'),
        default=constants.OPEN_TASK_STATUS,
        db_index=True,
    )
    type_of = models.PositiveSmallIntegerField(
        _("type_of"),
        choices=constants.TASK_TYPE_OPTIONS,
        help_text=_('The state this task in our application.'),
        default=constants.TASK_BY_CUSTOM_TYPE,
    )
    start = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_('The date/time this task will start.'),
    )
    is_due = models.BooleanField(
        _("Is Due"),
        help_text=_('Indicates whether this Task has a due date or not.'),
        default=False
    )
    due = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_('The date/time this task will finish.'),
    )
    assigned_by = models.ForeignKey(
        Me,
        help_text=_('The user whom assigned this task.'),
        blank=True,
        null=True,
        related_name="task_assigned_by_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    participants = models.ManyToManyField(
        Me,
        help_text=_('The users who are participating in this task.'),
        blank=True,
        related_name="task_participants_%(app_label)s_%(class)s_related"
    )
    opening = models.ManyToManyField(
        Me,
        help_text=_('The users who are not participating in this task.'),
        blank=True,
        related_name="task_opening_%(app_label)s_%(class)s_related"
    )
    closures = models.ManyToManyField(
        Me,
        help_text=_('The users who are participating in this task.'),
        blank=True,
        related_name="task_closures_%(app_label)s_%(class)s_related"
    )
    tags = models.ManyToManyField(
        Tag,
        help_text=_('The tags that belong to this Task.'),
        blank=True,
        related_name="task_tags_%(app_label)s_%(class)s_related"
    )
    comment_posts = models.ManyToManyField(                # CONTROLLED BY SYSTEM
        SortedCommentPostByCreated,
        help_text=_('The comment posts associated with this Task.'),
        blank=True,
        related_name='task_comment_posts_%(app_label)s_%(class)s_related',
    )
    log_events = models.ManyToManyField(                  # CONTROLLED BY SYSTEM & PRIVATE
        SortedLogEventByCreated,
        help_text=_('The log events associated with this Task.'),
        blank=True,
        related_name='task_log_events_%(app_label)s_%(class)s_related',
    )

    #----------------------#
    # Basic Task Fields    #
    #----------------------#
    # Nothing ...

    #----------------------#
    # Calendar Task Fields #
    #----------------------#
    # Nothing ...

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
        FileUpload,
        help_text=_('The files uploaded by a User.'),
        blank=True,
        related_name='task_uploads_%(app_label)s_%(class)s_related',
    )

    #----------------------#
    # Resource Task Fields #
    #----------------------#
    resources = models.ManyToManyField(
        InfoResource,
        help_text=_('The the InfoResources associated with this Task.'),
        blank=True,
        related_name="task_resources_%(app_label)s_%(class)s_related",
    )

    def __str__(self):
        return str(self.name)
