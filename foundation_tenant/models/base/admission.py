from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.tag import Tag


class AdmissionManager(models.Manager):
    def delete_all(self):
        items = Admission.objects.all()
        for item in items.all():
            item.delete()


class Admission(models.Model):
    class Meta:
        app_label = 'foundation_tenant'
        db_table = 'smeg_admission'
        verbose_name = _('Admission')
        verbose_name_plural = _('Admissions')

    objects = AdmissionManager()
    tag = models.OneToOneField(
        Tag,
        help_text=_('The Tag to handle our admission.'),
        on_delete=models.CASCADE,
    )
    users = models.ManyToManyField(
        User,
        help_text=_('The entrepreneur Users that belong to this program.'),
        blank=True,
        related_name="admission_users_%(app_label)s_%(class)s_related"
    )

    def __str__(self):
        return str(self.tag.name)
