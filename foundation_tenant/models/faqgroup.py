from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.faqitem import FAQItem
from foundation_tenant import constants


class FAQGroupManager(models.Manager):
    def delete_all(self):
        items = FAQGroup.objects.all()
        for item in items.all():
            item.delete()


class FAQGroup(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        ordering = ('created',)
        db_table = 'biz_faq_groups'
        verbose_name = 'FAQ Group'
        verbose_name_plural = 'FAQ Groups'

    objects = FAQGroupManager()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    text = models.TextField(
        _("Text"),
        help_text=_('The title text.'),
        blank=True,
        null=True,
    )
    items = models.ManyToManyField(
        FAQItem,
        help_text=_('The items inside this group.'),
        blank=True,
        related_name='faq_group_items_%(app_label)s_%(class)s_related',
    )

    def __str__(self):
        return str(self.text)
