from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.imageupload import PublicImageUpload
# from django.core.validators import MinValueValidator, MaxValueValidator
from foundation_public import constants


class BusinessIdea(models.Model):
    class Meta:
        app_label = 'foundation_public'
        db_table = 'biz_business_ideas'
        verbose_name = 'Business Idea'
        verbose_name_plural = 'Business Ideas'

    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        help_text=_('The user whom owns this thing.'),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    #TODO: Implement the rest.

    def __str__(self):
        return str(self.name)
