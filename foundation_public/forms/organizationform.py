from datetime import date
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, BooleanField
from django.forms.widgets import EmailInput, Select
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from foundation_public.models.organization import PublicOrganization


class PublicOrganizationForm(forms.ModelForm):
    class Meta:
        model = PublicOrganization
        fields = ['schema_name', 'name', 'url', 'facebook_url', 'twitter_url', 'how_many_served', 'how_discovered', 'is_tos_signed',]
        labels = {
            'schema_name': _('Sub-Domain'),
            'name': _('Name'),
            'url': _('Website'),
            'facebook_url': _('Facebook'),
            'twitter_url': _('Twitter'),
            'is_tos_signed': _('I agree to the terms.'),
        }
        widgets = {
            'schema_name': TextInput(attrs={
                'class': u'form-control input-lg',
                'placeholder': _('Enter sub-domain of this Organization.'),
                'autocapitalize':'off',
                'autocomplete':'off',
                'spellcheck':'false',
            }),
            'name': TextInput(attrs={
                'class': u'form-control input-lg',
                'placeholder': _('Enter name.'),
                'spellcheck':'false',
            }),
            'url': TextInput(attrs={
                'class': u'form-control input-lg',
                'placeholder': _('Enter website URL.'),
                'autocapitalize':'off',
                'autocomplete':'off',
            }),
            'facebook_url': TextInput(attrs={
                'class': u'form-control input-lg',
                'placeholder': _('Enter Facebook URL.'),
                'autocapitalize':'off',
                'autocomplete':'off',
            }),
            'twitter_url': TextInput(attrs={
                'class': u'form-control input-lg',
                'placeholder': _('Enter Twitter URL.'),
                'autocapitalize':'off',
                'autocomplete':'off',
            }),
            'how_many_served': Select(attrs={
                'class': u'form-control input-lg',
                'placeholder': _('Enter how many entrepreneurs served.'),
                'autocapitalize':'off',
                'autocomplete':'off',
            }),
            'how_discovered': Select(attrs={
                'class': u'form-control input-lg',
                'placeholder': _('How did you hear about SME Gurus?'),
                'autocapitalize':'off',
                'autocomplete':'off',
            }),
        }
