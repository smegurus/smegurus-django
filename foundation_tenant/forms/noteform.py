from datetime import date
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, BooleanField
from django.forms.widgets import EmailInput, Select
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.note import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['name', 'description',]
        labels = {
            'name': _('Title'),
            'description': _('Text'),
        }
        widgets = {
            'name': TextInput(attrs={
                'class': u'form-control',
                'placeholder': _('Enter title.')
            }),
            'description': Textarea(attrs={
                'class': u'form-control',
                'placeholder': _('Enter text.')
            }),
        }
