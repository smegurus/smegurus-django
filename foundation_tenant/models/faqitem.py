from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant import constants


class FAQItemManager(models.Manager):
    def delete_all(self):
        items = FAQItem.objects.all()
        for item in items.all():
            item.delete()


class FAQItem(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_faq_items'
        verbose_name = 'FAQ Item'
        verbose_name_plural = 'FAQ Items'

    objects = FAQItemManager()
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    question_text = models.CharField(
        _("Question"),
        max_length=255,
        help_text=_('The question text.'),
        blank=True,
        null=True,
    )
    answer_text = models.TextField(
        _("Answer"),
        help_text=_('The answer text.'),
        blank=True,
        null=True,
    )
    likers = models.ManyToManyField(
        User,
        help_text=_('The Users whom liked this item.'),
        blank=True,
        related_name='faq_item_likers_%(app_label)s_%(class)s_related',
    )
    dislikers = models.ManyToManyField(
        User,
        help_text=_('The Users whom disliked this item..'),
        blank=True,
        related_name='faq_item_dislikers_%(app_label)s_%(class)s_related',
    )

    def __str__(self):
        return str(self.owner.email)
