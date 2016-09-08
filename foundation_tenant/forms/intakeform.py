from datetime import date
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, BooleanField
from django.forms.widgets import EmailInput, Select
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.intake import Intake


class IntakeForm(forms.ModelForm):
    class Meta:
        model = Intake
        fields = ['how_can_we_help', 'how_can_we_help_other', 'how_can_we_help_tag',
        'how_did_you_hear', 'how_did_you_hear_other', 'do_you_own_a_biz',
        'do_you_own_a_biz_other', 'has_telephone', 'telephone',
        'telephone_time', 'government_benefits', 'identities']
        labels = {
            # 'name': _('Name'),
            # 'industry': _('Industry'),
            # 'image': _('Image'),
        }
        widgets = {
            'how_can_we_help': Select(attrs={
                'class': u'form-control',
            }),
            'how_can_we_help_other': TextInput(attrs={
                'class': u'form-control',
                # 'placeholder': _('Enter name.')
            }),
            'how_can_we_help_tag': Select(attrs={
                'class': u'form-control',
                # 'placeholder': _('Enter name.')
            }),
            'how_did_you_hear': Select(attrs={
                'class': u'form-control',
            }),
            'how_did_you_hear_other': TextInput(attrs={
                'class': u'form-control',
                # 'placeholder': _('Enter name.')
            }),

            'do_you_own_a_biz': Select(attrs={
                'class': u'form-control',
            }),
            'do_you_own_a_biz_other': TextInput(attrs={
                'class': u'form-control',
                # 'placeholder': _('Enter name.')
            }),

            'has_telephone': Select(attrs={
                'class': u'form-control',
            }),
            'telephone': TextInput(attrs={
                'class': u'form-control',
                # 'placeholder': _('Enter name.')
            }),
            'telephone_time': Select(attrs={
                'class': u'form-control',
            }),
        }
