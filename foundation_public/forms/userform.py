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
                'class': u'form-control',
                'placeholder': _('Enter First Name')
            }),
            'last_name': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter Last Name')
            }),
        }
    email = forms.EmailField(
        label='Email',
        max_length=30, # NOTE: Must be limited to "Username" field's limit.
        widget=forms.TextInput(attrs={
            'type':'email',
            'class':'form-control',
            'placeholder': _('Enter Email'),
            'spellcheck':'false',
        }),
        required=False,
    )
    old_password = forms.CharField(
        label='Old Password',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'password',
            'class':'form-control',
            'placeholder': _('Enter Old Password'),
            'autocomplete':'off',
            'spellcheck':'false',
        }),
        required=False,
    )

    password = forms.CharField(
        label='New Password',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'password',
            'class':'form-control',
            'placeholder': _('Enter New Password'),
            'autocomplete':'off',
            'spellcheck':'false',
        }),
        required=False,
    )

    password_repeated = forms.CharField(
        label='Repeat Password',
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'password',
            'class':'form-control',
            'placeholder': _('Enter Password Again'),
            'autocomplete':'off',
            'spellcheck':'false',
        }),
        required=False,
    )

    is_tos_signed = BooleanField(
        label=_('I agree to terms'),
        required=True
    )

    # def clean_password_repeated(self):
    #     password = self.cleaned_data['password']
    #     password_repeated = self.cleaned_data['password_repeated']
    #     if password != password_repeated:
    #         raise forms.ValidationError("Passwords do not match.")
    #     return password_repeated
