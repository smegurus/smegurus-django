# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 22:39
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foundation_tenant', '0004_auto_20161103_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='document_type',
            field=models.ForeignKey(blank=True, help_text='The document type this document is.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_document_typefoundation_tenant_document_related', to='foundation_tenant.DocumentType'),
        ),
        migrations.AddField(
            model_name='question',
            name='options',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank={}, help_text='The options to populate the question with.', null=True, verbose_name='Options'),
        ),
    ]
