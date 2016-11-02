from datetime import date
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, BooleanField
from django.forms.widgets import EmailInput, Select, CheckboxSelectMultiple
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from foundation_tenant.models.base.intake import Intake


class IntakeForm(forms.ModelForm):
    class Meta:
        model = Intake
        fields = ['how_can_we_help', 'how_can_we_help_other', 'how_can_we_help_tag',
        'how_did_you_hear', 'how_did_you_hear_other', 'do_you_own_a_biz',
        'do_you_own_a_biz_other', 'has_telephone', 'telephone',
        'telephone_time', 'government_benefits', 'other_government_benefit',
        'identities', 'date_of_birth', 'has_business_idea', 'naics_depth_one',
        'naics_depth_two', 'naics_depth_three', 'naics_depth_four', 'naics_depth_five',
        'has_signed_privacy_and_terms', 'has_signed_confidentiality_agreement',
        'has_signed_collection_and_use_of_information', 'has_signed_with_name',
        'has_signed_on_date',]
        labels = {
            'how_can_we_help_tag': _('Which program are you interested in?'),
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
            'government_benefits': CheckboxSelectMultiple(),
            'other_government_benefit': TextInput(attrs={
                'class': u'form-control',
                # 'placeholder': _('Enter name.')
            }),
            'identities': CheckboxSelectMultiple(),
            'date_of_birth': TextInput(attrs={
                'class': u'form-control',
            }),
            'naics_depth_one': Select(attrs={
                'class': u'form-control',
            }),
            'naics_depth_two': Select(attrs={
                'class': u'form-control',
            }),
            'naics_depth_three': Select(attrs={
                'class': u'form-control',
            }),
            'naics_depth_four': Select(attrs={
                'class': u'form-control',
            }),
            'naics_depth_five': Select(attrs={
                'class': u'form-control',
            }),
            'has_signed_with_name': TextInput(attrs={
                'class': u'form-control',
                # 'placeholder': _('Enter name.')
            }),
            'has_signed_on_date': TextInput(attrs={
                'class': u'form-control',
                # 'placeholder': _('Enter name.')
            }),
        }

#           'has_signed_privacy_and_terms', 'has_signed_confidentiality_agreement',
#           'has_signed_collection_and_use_of_information', 'has_signed_with_name',
#           'has_signed_on_date', 'privacy_note', 'terms_note', 'confidentiality_note',
#           'collection_note')
