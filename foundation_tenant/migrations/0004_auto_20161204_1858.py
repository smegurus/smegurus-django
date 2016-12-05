# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-04 23:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foundation_tenant', '0003_auto_20161204_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantme',
            name='level_of_education',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Some High School'), (2, 'High School diploma'), (3, 'Some Post-Secondary'), (4, 'Post-Secondary diploma'), (5, 'Graduate degree'), (6, 'Professional degree'), (7, 'Other')], default=1, help_text='The highest level of education this User has attained.', verbose_name='Highest Level of Education'),
        ),
    ]
