from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.abstract_creativework import AbstractCreativeWork
from foundation_tenant.models.base.me import Me


class MessageManager(models.Manager):
    def delete_all(self):
        items = Message.objects.all()
        for item in items.all():
            item.delete()


class Message(AbstractCreativeWork):
    """
    A single message from a sender to one or more organizations or people.

    https://schema.org/Message
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_messages'
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    objects = MessageManager()
    date_read = models.DateTimeField(
        _('Date Read'),
        help_text=_('The date/time at which the message has been read by the recipient if a single recipient exists.'),
        blank=True,
        null=True
    )
    date_received = models.DateTimeField(
        _('Date Received'),
        help_text=_('The date/time the message was received if a single recipient exists.'),
        blank=True,
        null=True,
        auto_now_add=True
    )
    date_sent = models.DateTimeField(
        _('Date Sent'),
        help_text=_('The date/time at which the message was sent.'),
        blank=True,
        null=True,
        auto_now_add=True
    )
    recipient = models.ForeignKey(
        Me,
        help_text=_('The user whom this message is sent to.'),
        blank=True,
        null=True,
        related_name="message_recipient_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        Me,
        help_text=_('The user whom this message originates from.'),
        blank=True,
        null=True,
        related_name="message_sender_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )
    participants = models.ManyToManyField(
        Me,
        help_text=_('The users who are participating in this message.'),
        blank=True,
        related_name="message_participants_%(app_label)s_%(class)s_related"
    )

    def __str__(self):
        return str(self.name)


# dateRead	DateTime
# dateReceived	DateTime
# dateSent	DateTime
