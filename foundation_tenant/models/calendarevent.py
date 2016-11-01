from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.me import TenantMe
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.tag import Tag
from smegurus import constants


class CalendarEventManager(models.Manager):
    def delete_all(self):
        items = CalendarEvent.objects.all()
        for item in items.all():
            item.delete()


class CalendarEvent(AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_calendar_events'
        verbose_name = 'Calendar Event'
        verbose_name_plural = 'Calendar Events'

    objects = CalendarEventManager()
    type_of = models.PositiveSmallIntegerField(
        _("type_of"),
        choices=constants.CALENDAR_EVENT_TYPE_OPTIONS,
        help_text=_('The state this intake application is in our application.'),
        default=constants.CALENDAR_EVENT_BY_CUSTOM_TYPE,
    )
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
    tags = models.ManyToManyField(
        Tag,
        help_text=_('The tags that belong to this event.'),
        blank=True,
        related_name="calendar_event_tags_%(app_label)s_%(class)s_related"
    )
    pending = models.ManyToManyField(
        TenantMe,
        help_text=_('The users who need to review whether they will attend this event or not.'),
        blank=True,
        related_name="calendar_event_pending_%(app_label)s_%(class)s_related"
    )
    attendees = models.ManyToManyField(
        TenantMe,
        help_text=_('The users who are participating in this event.'),
        blank=True,
        related_name="calendar_event_attendees_%(app_label)s_%(class)s_related"
    )
    absentees = models.ManyToManyField(
        TenantMe,
        help_text=_('The users who are participating in this event.'),
        blank=True,
        related_name="calendar_event_absentee_%(app_label)s_%(class)s_related"
    )

    def __str__(self):
        return str(self.name)


class SortedCalendarEventByCreated(CalendarEvent):
    class Meta:
        proxy = True
        app_label = 'foundation_tenant'
        db_table = 'smeg_sorted_calendar_events_by_created'
        ordering = ('-created',)
        verbose_name = _('Sorted by Created Calendar Event')
        verbose_name_plural = _('Sorted by Created Calendar Events')
