from datetime import date
from django.db import models
from django import forms
from django.forms.widgets import EmailInput
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_('Email'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'email',
            'class':'form-control',
            'placeholder':_('Enter Email'),
            'autocapitalize':'off',
            'autocomplete':'off',
            'data-parsley-id':'7556',
            'required':'',
            'spellcheck':'false',
        }),
    )
    password = forms.CharField(
        label=_('Password'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'type':'password',
            'class':'form-control',
            'placeholder':_('Enter Password'),
            'autocapitalize':'off',
            'autocomplete':'off',
            'data-parsley-id':'0276',
            'required':'',
            'spellcheck':'false',
        }),
    )
