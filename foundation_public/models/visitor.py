from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_public import constants
from foundation_public.models.abstract_bigpk import AbstractPublicBigPk


class PublicVisitorManager(models.Manager):
    def delete_all(self):
        items = PublicVisitor.objects.all()
        for item in items.all():
            item.delete()


class PublicVisitor(AbstractPublicBigPk):
    """The model used to store what URL location was visted and from what a IP."""
    class Meta:
        app_label = 'foundation_public'
        db_table = 'smeg_public_visitors'
        verbose_name = 'Public Visitor'
        verbose_name_plural = 'Public Visitors'

    objects = PublicVisitorManager()
    created = models.DateTimeField(auto_now_add=True)
    path = models.CharField(
        _("Path"),
        max_length=1027,
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
        return self.path in constants.SUSPICIOUS_PATHS


class SortedPublicVisitorsByLatestCreation(PublicVisitor):
    """
    Proxy model which will automatically return querys which are sorted
    by the lastest creation date.
    """
    class Meta:
        proxy = True
        app_label = 'foundation_public'
        ordering = ('-created',)
        verbose_name = _('Sorted Public Visitor by Latest Creation Date')
        verbose_name_plural = _('Sorted Public Visitors by Latest Creation Date')
