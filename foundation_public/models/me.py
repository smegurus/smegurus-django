from django.db import models
from django.utils.translation import ugettext_lazy as _
# from django.core.validators import MinValueValidator, MaxValueValidator
from foundation_public.models.abstract_person import AbstractPlacePerson
from foundation_public import constants


class PublicMe(AbstractPlacePerson):
    """
    The object that represents the entreprenuer.
    """
    class Meta:
        app_label = 'foundation_public'
        db_table = 'biz_mes'

    how_discovered = models.CharField(
        _("How user discovered SMEGurus"),
        choices=constants.HOW_DISCOVERED_OPTIONS,
        max_length=127,
        help_text=_('The details of how the User discovered our website.'),
        blank=True,
        null=True,
    )
    is_tos_signed = models.BooleanField(
        _("Is terms of service signed"),
        default=False
    )
    is_setup = models.BooleanField(
        _("Is this account setup and ready"),
        default=False,
        help_text=_('Variable controls whether the user profile has been setup.'),
    )

    def __str__(self):
        return str(self.name)
