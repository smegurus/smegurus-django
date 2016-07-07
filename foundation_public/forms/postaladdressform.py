from datetime import date
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, BooleanField
from django.forms.widgets import EmailInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.organization import PublicPostalAddress


class PublicPostalAddressForm(forms.ModelForm):
    class Meta:
        model = PublicPostalAddress
        fields = ['street_address', 'postal_code', 'address_locality', 'address_region', 'address_country', ] # 'post_office_box_number',
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
            'address_locality': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter the city name')
            }),
            'address_region': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter province name')
            }),
            'address_country': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter country')
            }),
        }
