from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing
from foundation_tenant.models.me import TenantMe


class CommunityAdvertisementManager(models.Manager):
    def delete_all(self):
        items = CommunityAdvertisement.objects.all()
        for item in items.all():
            item.delete()


class CommunityAdvertisement(AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        ordering = ('-created',)
        db_table = 'biz_community_advertisements'
        verbose_name = 'Community Advertisement'
        verbose_name_plural = 'Community Advertisements'

    objects = CommunityAdvertisementManager()

    def __str__(self):
        return str(self.name)
