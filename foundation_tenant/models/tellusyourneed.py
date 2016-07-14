from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class TellUsYourNeed(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_tell_us_your_needs'
        verbose_name = 'Tell Us Your Need'
        verbose_name_plural = 'Tell Us Your Needs'

    owner = models.OneToOneField(
        User,
        help_text=_('The user whom owns this thing.'),
        on_delete=models.CASCADE,
    )
    needs_financial_management = models.BooleanField(
        _("Needs Financial Management"),
        default=False,
        blank=True,
    )
    needs_sales = models.BooleanField(
        _("Needs Sales"),
        default=False,
        blank=True,
    )
    needs_social_media = models.BooleanField(
        _("Needs Social Media"),
        default=False,
        blank=True,
    )
    needs_other = models.BooleanField(
        _("Needs Other"),
        default=False,
        help_text=_('Indicates if we have other reasons.'),
        blank=True,
    )
    other = models.CharField(
        _("Other"),
        max_length=255,
        help_text=_('The text field for other.'),
        blank=True,
        null=True,
        default='',
    )

    def __str__(self):
        return str(self.id)
