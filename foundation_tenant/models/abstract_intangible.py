from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing


class AbstractIntangible(AbstractThing):
    """
    A utility class that serves as the umbrella for a number of 'intangible'
    things such as quantities, structured values, etc.

    https://schema.org/Intangible
    """
    class Meta:
        abstract = True
