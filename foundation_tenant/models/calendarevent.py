from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing


class CalendarEventManager(models.Manager):
    def delete_all(self):
        items = CalendarEvent.objects.all()
        for item in items.all():
            item.delete()


class CalendarEvent(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_calendar_events'
        verbose_name = 'Calendar Event'
        verbose_name_plural = 'Calendar Events'

    objects = CalendarEventManager()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        help_text=_('The user whom owns this thing.'),
        blank=True,
        null=True
    )
    name = models.CharField(
        _("Name"),
        max_length=127,
        help_text=_('The name of the Tag item.'),
        unique=True,
    )
    status = models.CharField(
        _("status"),
        max_length=63,
        help_text=_('The name of the Tag item.'),
        unique=True,
    )
    start = models.DateTimeField(
        blank=True,
        null=True,
    )
    finish = models.DateTimeField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)
