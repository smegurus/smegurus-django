from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.me import TenantMe


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
        verbose_name = 'Visitor'
        verbose_name_plural = 'Visitors'

    objects = VisitorManager()
    created = models.DateTimeField(auto_now_add=True)
    me = models.ForeignKey(
        TenantMe,
        help_text=_('The user whom owns this thing. Anonymous users have this field set to NULL.'),
        on_delete=models.CASCADE
    )
    path = models.CharField(
        _("Path"),
        max_length=63,
        help_text=_('The resource path that was visted.'),
    )
    ip_address = models.GenericIPAddressField(
        _("IP Address"),
        help_text=_('The location where the vistor is from.'),
    )

    def __str__(self):
        return str(self.path) + " by " + str(self.me.name)
