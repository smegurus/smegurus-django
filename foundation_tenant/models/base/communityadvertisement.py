from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.abstract_bigpk import AbstractBigPk
from foundation_tenant.models.base.abstract_thing import AbstractThing
from foundation_tenant.models.base.me import Me


class CommunityAdvertisementManager(models.Manager):
    def delete_all(self):
        items = CommunityAdvertisement.objects.all()
        for item in items.all():
            item.delete()


class CommunityAdvertisement(AbstractBigPk, AbstractThing):
    class Meta:
        app_label = 'foundation_tenant'
        ordering = ('-created',)
        db_table = 'smeg_community_advertisements'
        verbose_name = _('Community Advertisement')
        verbose_name_plural = _('Community Advertisements')

    objects = CommunityAdvertisementManager()

    def __str__(self):
        return str(self.name)
