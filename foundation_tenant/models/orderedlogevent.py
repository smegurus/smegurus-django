from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.me import TenantMe


class OrderedLogEventManager(models.Manager):
    def delete_all(self):
        items = OrderedLogEvent.objects.all()
        for item in items.all():
            item.delete()


class OrderedLogEvent(models.Model):
    """
    Model is to be used by our system to create log entries about various
    events. This model cannot be accessed by the API.
    """
    class Meta:
        app_label = 'foundation_tenant'
        ordering = ('created',)
        db_table = 'biz_ordered_log_events'
        verbose_name = 'Ordered Log Event'
        verbose_name_plural = 'Ordered Log Events'

    objects = OrderedLogEventManager()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    me = models.ForeignKey(
        TenantMe,
        help_text=_('The user whom caused this log event.'),
        blank=True,
        null=True,
        related_name="ordered_log_event_me_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    text = models.CharField(
        _("text"),
        max_length=125,
        help_text=_('The name of the TaskLog item.'),
        unique=True,
    )
    ip_address = models.GenericIPAddressField(
        _('IP Address'),
        help_text=_('The IP address that belongs to the User associated with this event.'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.text)
