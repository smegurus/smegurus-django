from django.db import models


class BannedDomain(models.Model):
    name = models.CharField(max_length=63, db_index=True, unique=True)
    banned_on = models.DateField(auto_now_add=True, null=True)
    reason = models.CharField(max_length=127, blank=True, null=True)

    class Meta:
        app_label = 'foundation'
        ordering = ('name',)
        db_table = 'den_banned_domains'

    def __str__(self):
        return str(self.name)


class BannedIP(models.Model):
    address = models.GenericIPAddressField(db_index=True, unique=True)
    banned_on = models.DateField(auto_now_add=True, null=True)
    reason = models.CharField(max_length=127, blank=True, null=True)

    class Meta:
        app_label = 'foundation'
        ordering = ('address',)
        db_table = 'den_banned_ips'

    def __str__(self):
        return str(self.address)


class BannedWord(models.Model):
    text = models.CharField(max_length=63, db_index=True, unique=True)
    banned_on = models.DateField(auto_now_add=True, null=True)
    reason = models.CharField(max_length=127, blank=True, null=True)

    class Meta:
        app_label = 'foundation'
        ordering = ('text',)
        db_table = 'den_banned_words'

    def __str__(self):
        return str(self.text)
