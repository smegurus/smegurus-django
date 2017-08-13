from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.abstract_bigpk import AbstractBigPk
from foundation_tenant.models.base.abstract_thing import AbstractThing
from foundation_tenant.models.base.me import Me


class NotificationManager(models.Manager):
    def delete_all(self):
        items = Notification.objects.all()
        for item in items.all():
            item.delete()


class Notification(AbstractThing, AbstractBigPk):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_notifications'
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    objects = NotificationManager()
    closures = models.ManyToManyField(
        Me,
        help_text=_('The users who closed the notification.'),
        blank=True,
        related_name="%(app_label)s_%(class)s_notification_closures_related"
    )
    icon = models.CharField(
        _("Icon"),
        max_length=31,
        help_text=_('The icon of this notification.'),
        blank=True,
        null=True,
    )
    type_of = models.CharField(
        _("Colour"),
        max_length=15,
        help_text=_('The colour of this notification.'),
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.name)
