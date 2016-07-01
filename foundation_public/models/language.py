from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.abstract_thing import AbstractPublicThing


class PublicLanguage(AbstractPublicThing):
    """
    Natural languages such as Spanish, Tamil, Hindi, English, etc. and programming languages such as Scheme and Lisp.

    https://schema.org/ContactPoint
    """
    class Meta:
        app_label = 'foundation_public'
        db_table = 'biz_languages'
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return str(self.name)
