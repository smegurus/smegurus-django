from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.me import TenantMe


class LogEventManager(models.Manager):
    def delete_all(self):
        items = LogEvent.objects.all()
        for item in items.all():
            item.delete()


class LogEvent(models.Model):
    """
    Model is to be used by our system to create log entries about various
    events. This model cannot be accessed by the API.
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_log_events'
        verbose_name = _('Log Event')
        verbose_name_plural = _('Log Events')

    objects = LogEventManager()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    me = models.ForeignKey(
        TenantMe,
        help_text=_('The user whom caused this log event.'),
        blank=True,
        null=True,
        related_name="log_event_me_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    text = models.CharField(
        _("text"),
        max_length=125,
        help_text=_('The details.'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.text)


class SortedLogEventByCreated(LogEvent):
    class Meta:
        proxy = True
        app_label = 'foundation_tenant'
        db_table = 'biz_sorted_log_events_by_created'
        ordering = ('created',)
        verbose_name = _('Sorted by Created Log Event')
        verbose_name_plural = _('Sorted by Created Log Events')
