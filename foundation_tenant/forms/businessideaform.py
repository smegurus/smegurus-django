from datetime import date
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, BooleanField
from django.forms.widgets import EmailInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.businessidea import BusinessIdea


class BusinessIdeaForm(forms.ModelForm):
    class Meta:
        model = BusinessIdea
        fields = ['name', 'industry', 'image',]
        labels = {
            'name': _('Name'),
            'industry': _('Industry'),
            'image': _('Image'),
        }
        # widgets = {
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
        # }