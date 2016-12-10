# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-10 01:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foundation_tenant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenttype',
            name='stage_num',
            field=models.PositiveSmallIntegerField(default=1, help_text='Track what stage this Document belongs to.', verbose_name='Stage Number'),
        ),
    ]
