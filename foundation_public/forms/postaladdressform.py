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
                  'street_name', 'street_type', 'direction', 'suite_number',
                  'floor_number', 'buzz_number', 'address_line_2',
                  'address_line_3',]
        labels = {
            'street_address': _('Street Address'),
            'postal_code': _('Postal Code/Zip'),
            'address_locality': _('City'),
            'address_region': _('Province/State'),
            'address_country': _('Country'),
        }
        widgets = {
            'street_address': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter the street address.')
            }),
            'postal_code': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter the postal code')
            }),
            'post_office_box_number': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter the postal code')
            }),
            'address_country': Select(attrs={
                'class': u'form-control',
                'placeholder': _('Enter country')
            }),
            'address_region': Select(attrs={
                'class': u'form-control',
                'placeholder': _('Enter province name')
            }),
            'address_locality': Select(attrs={
                'class': u'form-control',
                'placeholder': _('Enter the city name')
            }),
        }
