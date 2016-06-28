from django.db import models
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

    auto_create_schema = True
    auto_drop_schema = True


class Domain(DomainMixin):
    pass
