from django.db import models
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.abstract_thing import AbstractThing


class LanguageManager(models.Manager):
    def delete_all(self):
        items = Language.objects.all()
        for item in items.all():
            item.delete()


class Language(AbstractThing):
    """
    Natural languages such as Spanish, Tamil, Hindi, English, etc. and programming languages such as Scheme and Lisp.

    https://schema.org/ContactPoint
    """
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_languages'
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    objects = LanguageManager()

    def __str__(self):
        return str(self.name)
