from datetime import date
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, BooleanField
from django.forms.widgets import EmailInput, Select
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.organization import PublicPostalAddress


class PublicPostalAddressForm(forms.ModelForm):
    class Meta:
        model = PublicPostalAddress
        fields = ['id', 'name', 'alternate_name', 'description', 'owner', 'url',
                  'country', 'postal_code', 'locality', 'region',
                  'street_number', 'suffix',
                  'street_name', 'suite_number', 'address_line_2',
                  'address_line_3',]
        labels = {
            'street_number': _('Street #'),
            'postal_code': _('Postal Code/Zip'),
            'locality': _('City'),
            'region': _('Province/State'),
            'suite_number': _('Suite #'),
            'address_line_2': _('Address Line 2'),
            'address_line_3': _('Address Line 3'),
        }
        widgets = {
            'street_number': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter the street number.')
            }),
            'street_name': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter the street name.')
            }),
            'postal_code': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter the postal code')
            }),
            'country': Select(attrs={
                'class': u'form-control',
            }),
            'region': Select(attrs={
                'class': u'form-control',
            }),
            'locality': Select(attrs={
                'class': u'form-control',
            }),
            'suffix': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter the suffix (Option).')
            }),
            'suite_number': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter the suite number.')
            }),
            'address_line_2': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter the address line 2.')
            }),
            'address_line_3': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter the address line 3.')
            }),
        }
