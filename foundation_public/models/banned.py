from django.db import models
from django.utils.translation import ugettext_lazy as _


class BannedDomain(models.Model):
    name = models.CharField(max_length=63, db_index=True, unique=True)
    banned_on = models.DateField(auto_now_add=True, null=True)
    reason = models.CharField(max_length=127, blank=True, null=True)

    class Meta:
        app_label = 'foundation_public'
        ordering = ('name',)
        db_table = 'smeg_banned_domains'

    def __str__(self):
        return str(self.name)


class AlphabeticallySortedBannedDomain(BannedDomain):
    """
    Proxy model which will automatically return querys which are sorted
    alphabetically by the domain.
    """
    class Meta:
        proxy = True
        app_label = 'foundation_public'
        ordering = ('-name',)
        verbose_name = _('Alphabetically Sorted Banned Domain')
        verbose_name_plural = _('Alphabetically Sorted Banned Domains')


class BannedIP(models.Model):
    address = models.GenericIPAddressField(db_index=True, unique=True)
    banned_on = models.DateField(auto_now_add=True, null=True)
    reason = models.CharField(max_length=127, blank=True, null=True)

    class Meta:
        app_label = 'foundation_public'
        ordering = ('address',)
        db_table = 'smeg_banned_ips'

    def __str__(self):
        return str(self.address)

# DEVELOPER NOTE:
# Run the following code in your server to get the latest IP list of banned users.
# PROD: python manage.py dumpdata --indent 4 --format=json foundation_public.BannedIP > ~/banned_ip.json


class SortedBannedIPByLatestCreationDate(BannedIP):
    """
    Proxy model which will automatically return querys which are sorted
    by latest creation date.
    """
    class Meta:
        proxy = True
        app_label = 'foundation_public'
        ordering = ('-banned_on',)
        verbose_name = _('Sorted Banned IP By Latest Creation Date')
        verbose_name_plural = _('Sorted Banned IPs By Latest Creation Date')


class BannedWord(models.Model):
    text = models.CharField(max_length=63, db_index=True, unique=True)
    banned_on = models.DateField(auto_now_add=True, null=True)
    reason = models.CharField(max_length=127, blank=True, null=True)

    class Meta:
        app_label = 'foundation_public'
        ordering = ('text',)
        db_table = 'smeg_banned_words'

    def __str__(self):
        return str(self.text)


class AlphabeticallySortedBannedWord(BannedWord):
    """
    Proxy model which will automatically return querys which are sorted
    alphabetically by the word.
    """
    class Meta:
        proxy = True
        app_label = 'foundation_public'
        ordering = ('-text',)
        verbose_name = _('Alphabetically Sorted Banned Word')
        verbose_name_plural = _('Alphabetically Sorted Banned Words')
