from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.me import TenantMe


class OrderedCommentPostManager(models.Manager):
    def delete_all(self):
        items = OrderedCommentPost.objects.all()
        for item in items.all():
            item.delete()


class OrderedCommentPost(AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        ordering = ('created',)
        db_table = 'biz_ordered_comment_posts'
        verbose_name = 'Ordered Comment'
        verbose_name_plural = 'Ordered Comments'

    objects = OrderedCommentPostManager()
    me = models.ForeignKey(
        TenantMe,
        help_text=_('The user whom this comment belongs to.'),
        blank=True,
        null=True,
        related_name="ordered_comment_post_me_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.description)
