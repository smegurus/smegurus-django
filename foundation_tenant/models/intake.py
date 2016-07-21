from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.tag import Tag


class IntakeManager(models.Manager):
    def delete_all(self):
        items = Intake.objects.all()
        for item in items.all():
            item.delete()


class Intake(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'biz_intake'
        verbose_name = 'Intake'
        verbose_name_plural = 'Intakes'

    objects = IntakeManager()
    owner = models.OneToOneField(
        User,
        help_text=_('The User that this Intake belongs to.'),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.owner.email)
