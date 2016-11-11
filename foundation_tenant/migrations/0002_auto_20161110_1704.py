# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foundation_tenant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenttype',
            name='is_master',
            field=models.BooleanField(default=False, help_text='Variable controls whether the Module this Document belongs to is the master document of the Module.', verbose_name='Is Master'),
        ),
        migrations.AddField(
            model_name='tenantme',
            name='manages',
            field=models.ManyToManyField(blank=True, help_text='The Users whom that this User manages.', related_name='_tenantme_manages_+', to='foundation_tenant.TenantMe'),
        ),
        migrations.AlterField(
            model_name='tenantme',
            name='stage_num',
            field=models.PositiveSmallIntegerField(db_index=True, default=0, help_text='Track what stage this User is in the system (If they are an entrepreneur).', verbose_name='Stage Number'),
        ),
    ]