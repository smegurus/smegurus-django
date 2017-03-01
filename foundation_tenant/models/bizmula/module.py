from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class ModuleManager(models.Manager):
    def delete_all(self):
        items = Module.objects.all()
        for item in items.all():
            item.delete()


class Module(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_modules'
        verbose_name = _('Module')
        verbose_name_plural = _('Modules')

    # ------------
    #   GENERIC
    # ------------

    objects = ModuleManager()

    # ------------
    #  NAVIGATION
    # ------------

    stage_num = models.PositiveSmallIntegerField(
        _("Stage Number"),
        help_text=_('Track what stage this Module belongs to.'),
        default=1,
        db_index=True,
    )
    nodes = JSONField( # https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#jsonfield
        _("Nodes"),
        help_text=_('The slides and Questions nodes to be processed by this module.'),
        blank=True,
        default="[]"
    )

    # ------------
    #  CONTENT
    # ------------

    title = models.CharField(
        _("Title"),
        max_length=127,
        help_text=_('The title of this Module.'),
        blank=True,
        null=True,
    )
    description = models.TextField(
        _("Description"),
        help_text=_('A description of this Module.'),
        blank=True,
        null=True,
        default='',
    )
    icon = models.CharField(
        _("Icon"),
        max_length=31,
        help_text=_('The icon to display for this Module.'),
        blank=True,
        null=True,
    )
    colour = models.CharField(
        _("Colour"),
        max_length=31,
        help_text=_('The colour to display for this Module.'),
        blank=True,
        null=True,
    )

    # ------------
    #  FUNCTIONS
    # ------------

    def __str__(self):
        return str(self.title)

    def get_node(self, target_id):
        return self.nodes[target_id]

    def get_first_node(self):
        try:
            return self.nodes[0]
        except Exception as e:
            return None

    def get_last_node(self):
        last_index = len(self.nodes)
        if last_index >= 0:
            return self.nodes[last_index-1]
        else:
            return None

    def get_document_type_id(self):
        """Return the 'document_type' identification of this model."""
        for node in self.nodes:
            return node['document_type']
        return None
