from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.abstract_thing import AbstractThing
from smegurus import constants


class CalendarEventManager(models.Manager):
    def delete_all(self):
        items = CalendarEvent.objects.all()
        for item in items.all():
            item.delete()


class CalendarEvent(AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_calendar_events'
        verbose_name = 'Calendar Event'
        verbose_name_plural = 'Calendar Events'

    objects = CalendarEventManager()
    colour = models.CharField(
        _("Colour"),
        max_length=31,
        help_text=_('The colour of the item.'),
        blank=True,
        null=True,
    )
    start = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_('The date/time this event starts on.'),
    )
    finish = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_('The date/time this event will finish.'),
    )
    participants = models.ManyToManyField(
        TenantMe,
        help_text=_('The users who are participating in this event.'),
        blank=True,
        related_name="calendar_event_participants_%(app_label)s_%(class)s_related"
    )
    status = models.PositiveSmallIntegerField(            # CONTROLLED BY SYSTEM
        _("Status"),
        choices=constants.STATUS_OPTIONS,
        help_text=_('The state this task.'),
        default=constants.CREATED_STATUS,
        db_index=True,
    )

    def __str__(self):
        return str(self.name)
