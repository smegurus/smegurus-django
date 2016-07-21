from datetime import date
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, BooleanField
from django.forms.widgets import EmailInput, Select
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.tag import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'is_program',]
        labels = {
            'name': _('Name'),
            'is_program': _('Is Program'),
        }
        widgets = {
            # 'industry': Select(attrs={
            #     'class': u'form-control',
            # }),
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
