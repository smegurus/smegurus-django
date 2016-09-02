from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.me import TenantMe


class TenantVisitorManager(models.Manager):
    def delete_all(self):
        items = TenantVisitor.objects.all()
        for item in items.all():
            item.delete()


class TenantVisitor(models.Model):
    """The model used to store what URL location was visted and from what User/IP."""
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_tenant_visitors'
        verbose_name = 'Tenant Visitor'
        verbose_name_plural = 'Tenant Visitors'

    objects = TenantVisitorManager()
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
