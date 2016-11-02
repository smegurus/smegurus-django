import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.countryoption import CountryOption
from foundation_tenant.models.base.provinceoption import ProvinceOption


class WorkspaceManager(models.Manager):
    def delete_all(self):
        items = Workspace.objects.all()
        for item in items.all():
            item.delete()


class Workspace(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_workspaces'
        verbose_name = 'Workspace'
        verbose_name_plural = 'Workspaces'

    objects = WorkspaceManager()
    name = models.CharField(
        _("Name"),
        max_length=63,
        help_text=_('The name of the City.'),
        blank=True,
        null=True,
    )
    owners = models.ManyToManyField(
        User,
        help_text=_('The owners of this workspace.'),
        blank=True,
        related_name="workspace_owners_%(app_label)s_%(class)s_related"
    )

    def __str__(self):
        return str(self.name)
