from datetime import date
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, BooleanField
from django.forms.widgets import EmailInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.me import PublicMe


class PublicMeForm(forms.ModelForm):
    class Meta:
        model = PublicMe
        fields = ['url', 'how_discovered', 'is_tos_signed',]
        labels = {
            'how_discovered': _('How did you hear about SME Gurus?'),
            'is_tos_signed': _('Name'),
            'url': _('Website'),
        }
        widgets = {
        #     'schema_name': TextInput(attrs={
        #         'class': u'form-control',
        #         'placeholder': _('Enter sub-domain of this Organization.')
        #     }),
        #     'name': TextInput(attrs={
        #         'class': u'form-control',
        #         'placeholder': _('Enter name.')
        #     }),
        #     'url': TextInput(attrs={
        #         'class': u'form-control',
        #         'placeholder': _('Enter website URL.')
        #     }),
        #     'facebook_url': TextInput(attrs={
        #         'class': u'form-control',
        #         'placeholder': _('Enter Facebook URL.')
        #     }),
        #     'twitter_url': TextInput(attrs={
        #         'class': u'form-control',
        #         'placeholder': _('Enter Twitter URL.')
        #     }),
        }
