from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.tag import Tag
from foundation_tenant.models.base.abstract_thing import AbstractThing
from foundation_tenant.models.base.me import Me


class CommunityPostManager(models.Manager):
    def delete_all(self):
        items = CommunityPost.objects.all()
        for item in items.all():
            item.delete()


class CommunityPost(AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        ordering = ('-created',)
        db_table = 'smeg_community_posts'
        verbose_name = 'Community Post'
        verbose_name_plural = 'Community Posts'

    objects = CommunityPostManager()
    tags = models.ManyToManyField(
        Tag,
        help_text=_('The tags that this User belongs to.'),
        blank=True,
        related_name="community_post_tags_%(app_label)s_%(class)s_related"
    )
    likers = models.ManyToManyField(
        User,
        help_text=_('The Users whom liked this post.'),
        blank=True,
        related_name="community_post_likers_%(app_label)s_%(class)s_related"
    )
    me = models.ForeignKey(
        Me,
        help_text=_('The user whom owns this thing.'),
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.name)
