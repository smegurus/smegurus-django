from datetime import date
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, BooleanField, EmailField
from django.forms.widgets import EmailInput
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _('Email'),
        }
        widgets = {
            'first_name': TextInput(attrs={
                'class': u'form-control input-lg',
                'placeholder': _('Enter First Name')
            }),
            'last_name': TextInput(attrs={
                'class': u'form-control input-lg',
                'placeholder': _('Enter Last Name')
            }),
        }
    email = forms.EmailField(
        label='Email',
        max_length=75, 
        widget=forms.TextInput(attrs={
            'type':'email',
            'class':'form-control input-lg',
            'placeholder': _('Enter Email'),
            'spellcheck':'false',
            'autocapitalize':'off',
            'autocomplete':'off',
        }),
        required=False,
    )
    old_password = forms.CharField(
        label='Old Password',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'password',
            'class':'form-control input-lg',
            'placeholder': _('Enter Old Password'),
            'spellcheck':'false',
            'autocapitalize':'off',
            'autocomplete':'off',
        }),
        required=False,
    )

    password = forms.CharField(
        label='New Password',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'password',
            'class':'form-control input-lg',
            'placeholder': _('Enter New Password'),
            'spellcheck':'false',
            'autocapitalize':'off',
            'autocomplete':'off',
        }),
        required=False,
    )

    password_repeated = forms.CharField(
        label='Repeat Password',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'password',
            'class':'form-control input-lg',
            'placeholder': _('Enter Password Again'),
            'spellcheck':'false',
            'autocapitalize':'off',
            'autocomplete':'off',
        }),
        required=False,
    )

    is_tos_signed = BooleanField(
        label=_('I agree to terms'),
        required=True
    )
