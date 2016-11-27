# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 01:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foundation_tenant', '0005_question_validation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='template_id',
        ),
        migrations.AddField(
            model_name='question',
            name='type_id',
            field=models.PositiveSmallIntegerField(blank=True, default=0, help_text='The question type ID to load up for the view.', null=True, verbose_name='Type ID'),
        ),
    ]