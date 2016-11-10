# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 23:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foundation_tenant', '0002_auto_20161110_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenantme',
            name='manages',
        ),
        migrations.AddField(
            model_name='tenantme',
            name='managed_by',
            field=models.ForeignKey(blank=True, help_text='The Users whom manages this User.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tenant_me_managed_by_foundation_tenant_tenantme_related', to='foundation_tenant.TenantMe'),
        ),
    ]
