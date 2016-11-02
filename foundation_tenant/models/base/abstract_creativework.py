from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.abstract_thing import AbstractThing


class AbstractCreativeWork(AbstractThing):
    """
    The most generic kind of creative work, including books, movies, photographs, software programs, etc.

    https://schema.org/CreativeWork
    """
    class Meta:
        abstract = True
