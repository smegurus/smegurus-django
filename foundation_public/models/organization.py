from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_tenants.models import TenantMixin, DomainMixin


class Organization(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until =  models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
    )
    on_trial = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        help_text=_('The user whom owns this thing.'),
        blank=True,
        null=True
    )

    auto_create_schema = True
    auto_drop_schema = True


class Domain(DomainMixin):
    pass
