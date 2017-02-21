from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.abstract_thing import AbstractThing
from foundation_tenant.models.base.me import Me


class CommentPostManager(models.Manager):
    def delete_all(self):
        items = CommentPost.objects.all()
        for item in items.all():
            item.delete()


class CommentPost(AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_comment_posts'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    objects = CommentPostManager()
    me = models.ForeignKey(
        Me,
        help_text=_('The user whom this comment belongs to.'),
        blank=True,
        null=True,
        related_name="comment_post_me_%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.description)


class SortedCommentPostByCreated(CommentPost):
    class Meta:
        proxy = True
        app_label = 'foundation_tenant'
        db_table = 'smeg_sorted_comment_posts_by_created'
        ordering = ('created',)
        verbose_name = 'Sorted Comment by Created'
        verbose_name_plural = 'Sorted Comments by Created'
