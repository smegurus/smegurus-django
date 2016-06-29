from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_tenants.models import TenantMixin, DomainMixin
from foundation_public.models.imageupload import PublicImageUpload


class Organization(TenantMixin):
    name = models.CharField(
        _("Name"),
        max_length=100
    )
    alternate_name = models.CharField(
        _("Alternate Name"),
        max_length=255,
        help_text=_('An alias for the item.'),
        blank=True,
        null=True,
    )
    description = models.TextField(
        _("Description"),
        help_text=_('A short description of the item.'),
        blank=True,
        null=True,
    )
    image = models.ForeignKey(
        PublicImageUpload,
        help_text=_('An image of the item.'),
        null=True,
        blank=True,
        related_name="thing_image_%(app_label)s_%(class)s_related"
    )

    # Payment Information
    on_trial = models.BooleanField(default=False)
    paid_until =  models.DateField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    # Ownership
    owner = models.ForeignKey(
        User,
        help_text=_('The user whom owns this thing.'),
        blank=True,
        null=True
    )

    # Misc
    created_on = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    auto_create_schema = True
    auto_drop_schema = True


class Domain(DomainMixin):
    pass
