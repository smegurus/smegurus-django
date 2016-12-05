from datetime import date
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, BooleanField
from django.forms.widgets import EmailInput, Select
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.me import TenantMe


class TenantMeForm(forms.ModelForm):
    class Meta:
        model = TenantMe
        fields = ['gender', 'gender_other', 'level_of_education', 'level_of_education_other',
        'place_of_birth', 'place_of_birth_other', 'employment_status', 'employment_status_other',
        'education_or_training_status', 'education_or_training_status_other', 'why_be_entrepreneur',
        'why_be_entrepreneur_other', 'challenges_becoming_entrepreneur', 'challenges_becoming_entrepreneur_other',
        'annual_income_bracket', 'has_owned_business', 'has_owned_business_other']
        labels = {
            # 'name': _('Name'),
            # 'industry': _('Industry'),
            # 'image': _('Image'),
        }
        widgets = {
            'place_of_birth': Select(attrs={
                'class': u'form-control',
            }),
        #     'name': TextInput(attrs={
        #         'class': u'form-control',
        #         'placeholder': _('Enter name.')
        #     }),
        #     'url': TextInput(attrs={
        #         'class': u'form-control',
        #         'placeholder': _('Enter website URL.')
        #     }),
        #     'facebook_url': TextInput(attrs={
        #         'class': u'form-control',
        #         'placeholder': _('Enter Facebook URL.')
        #     }),
        #     'twitter_url': TextInput(attrs={
        #         'class': u'form-control',
        #         'placeholder': _('Enter Twitter URL.')
        #     }),
        }
