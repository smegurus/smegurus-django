from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.tag import Tag
from foundation_tenant.models.abstract_thing import AbstractThing


class TenantMeManager(models.Manager):
    def get_by_owner_or_none(self, owner):
        try:
            return TenantMe.objects.get(owner=owner)
        except TenantMe.DoesNotExist:
            return None

    def delete_all(self):
        items = TenantMe.objects.all()
        for item in items.all():
            item.delete()


class TenantMe(models.Model):
    """
    The object to represent the "PublicMe" object for all the tenanted objects.
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_tenant_mes'
        verbose_name = 'Tenant Me'
        verbose_name_plural = 'Tenant Mes'

    objects = TenantMeManager()
    owner = models.OneToOneField(
        User,
        help_text=_('The user whom owns this thing.'),
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(
        Tag,
        help_text=_('The tags that this User belongs to.'),
        blank=True,
        related_name="tenant_me_tags_%(app_label)s_%(class)s_related"
    )

    def __str__(self):
        return str(self.id)
