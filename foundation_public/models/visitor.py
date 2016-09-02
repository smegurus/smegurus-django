from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class PublicVisitorManager(models.Manager):
    def delete_all(self):
        items = PublicVisitor.objects.all()
        for item in items.all():
            item.delete()


class PublicVisitor(models.Model):
    """The model used to store what URL location was visted and from what a IP."""
    class Meta:
        app_label = 'foundation_public'
        db_table = 'biz_public_visitors'
        verbose_name = 'Public Visitor'
        verbose_name_plural = 'Public Visitors'

    objects = PublicVisitorManager()
    created = models.DateTimeField(auto_now_add=True)
    path = models.CharField(
        _("Path"),
        max_length=63,
        help_text=_('The resource path that was visted.'),
    )
    ip_address = models.GenericIPAddressField(
        _("IP Address"),
        help_text=_('The location where the vistor is from.'),
    )
    is_suspicious = models.BooleanField(
        default=False,
        help_text=_('Variable indicates whether this visitor has malicious intent.'),
    )

    def __str__(self):
        return str(self.path) + " by " + str(self.ip_address)

    def is_path_suspicious(self):
        """
        Function will lookup this path in a list of suspicious paths and
        return a True/False depending on if this path exists in the suspicious
        list.
        """
        suspicious_paths = [
            '/phpMyAdmin/scripts/setup.php',
            '/pma/scripts/setup.php',
            '/myadmin/scripts/setup.php',
            '/HNAP1/',
        ]
        return self.path in suspicious_paths
