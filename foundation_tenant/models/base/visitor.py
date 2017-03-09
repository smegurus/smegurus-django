from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.me import Me


class VisitorManager(models.Manager):
    def delete_all(self):
        items = Visitor.objects.all()
        for item in items.all():
            item.delete()


class Visitor(models.Model):
    """The model used to store what URL location was visted and from what User/IP."""
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_visitors'
        verbose_name = _('Visitor')
        verbose_name_plural = _('Visitors')

    objects = VisitorManager()
    created = models.DateTimeField(auto_now_add=True)
    me = models.ForeignKey(
        Me,
        help_text=_('The user whom owns this thing. Anonymous users have this field set to NULL.'),
        on_delete=models.CASCADE
    )
    path = models.CharField(
        _("Path"),
        max_length=1027,
        help_text=_('The resource path that was visted.'),
    )
    ip_address = models.GenericIPAddressField(
        _("IP Address"),
        help_text=_('The location where the vistor is from.'),
    )

    def __str__(self):
        return str(self.path) + " by " + str(self.me.name)



class SortedVisitorsByLatestCreation(Visitor):
    """
    Proxy model which will automatically return querys which are sorted
    by the lastest creation date.
    """
    class Meta:
        proxy = True
        app_label = 'foundation_tenant'
        ordering = ('-created',)
        verbose_name = _('Sorted Visitor by Latest Creation')
        verbose_name_plural = _('Sorted Visitors by Latest Creation')
