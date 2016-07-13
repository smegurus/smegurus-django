from datetime import date
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, BooleanField
from django.forms.widgets import EmailInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.tellusyourneed import TellUsYourNeed


class TellUsYourNeedForm(forms.ModelForm):
    class Meta:
        model = TellUsYourNeed
        fields = ['needs_financial_management', 'needs_sales', 'needs_social_media', 'needs_other', 'other']
        labels = {
            'needs_financial_management': _('Financial Management'),
            'needs_sales': _('Sales'),
            'needs_social_media': _('Social Media'),
            'needs_other': _('Other'),
            'other': _('Other Text'),
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
