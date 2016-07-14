from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.imageupload import TenantImageUpload
from foundation_public import constants


INDUSTRY_OPTIONS = (
    (1, _('Construction')),
    (2, _('Business')),
    (3, _('Other')),
)

class BusinessIdea(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_business_ideas'
        verbose_name = 'Business Idea'
        verbose_name_plural = 'Business Ideas'

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        help_text=_('The user whom owns this thing.'),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_('The name of the item.'),
        blank=True,
        null=True,
        default='',
    )
    industry = models.PositiveSmallIntegerField(
        _("Name"),
        choices=INDUSTRY_OPTIONS,
        help_text=_('The industry that this Business Idea belongs to.'),
        blank=True,
        default=1,
    )
    image = models.ForeignKey(
        TenantImageUpload,
        help_text=_('An image of the item.'),
        null=True,
        blank=True,
        related_name="business_idea_image_%(app_label)s_%(class)s_related"
    )

    def __str__(self):
        return str(self.name)
