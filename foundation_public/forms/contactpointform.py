from datetime import date
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, BooleanField
from django.forms.widgets import EmailInput, Select
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.contactpoint import PublicContactPoint


class PublicContactPointForm(forms.ModelForm):
    class Meta:
        model = PublicContactPoint
        fields = ['email', 'telephone', 'fax_number']
        labels = {
            'email': _('Email'),
            'telephone': _('Telephone'),
            'fax_number': _('Fax Number'),
        }
        widgets = {
            'email': TextInput(attrs={
                'class': u'form-control input-lg',
                'placeholder': _('Enter the email.')
            }),
            'telephone': TextInput(attrs={
                'class': u'form-control input-lg',
                'placeholder': _('Enter the telephone.')
            }),
            'fax_number': TextInput(attrs={
                'class': u'form-control input-lg',
                'placeholder': _('Enter the fax number.')
            }),
        }
