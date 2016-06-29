# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 19:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foundation_tenant', '0006_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('alternate_name', models.CharField(blank=True, help_text='An alias for the item.', max_length=255, null=True, verbose_name='Alternate Name')),
                ('description', models.TextField(blank=True, help_text='A short description of the item.', null=True, verbose_name='Description')),
                ('main_entity_of_page', models.URLField(blank=True, help_text='Indicates a page for which this thing is the main entity being described.', null=True, verbose_name='Main Entity Of Page')),
                ('name', models.CharField(blank=True, help_text='The name of the item.', max_length=255, null=True, verbose_name='Name')),
                ('same_as', models.URLField(blank=True, help_text="URL of a reference Web page that unambiguously indicates the item's identity. E.g. the URL of the item's Wikipedia page, Freebase page, or official website.", null=True, verbose_name='Same As')),
                ('url', models.URLField(blank=True, help_text='URL of the item.', null=True, verbose_name='URL')),
                ('image', models.ForeignKey(blank=True, help_text='An image of the item.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thing_image_foundation_tenant_brand_related', to='foundation_tenant.TenantImageUpload')),
                ('logo', models.ForeignKey(blank=True, help_text='An associated logo.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_logo', to='foundation_tenant.TenantImageUpload')),
                ('owner', models.ForeignKey(blank=True, help_text='The user whom owns this thing.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Brands',
                'verbose_name': 'Brand',
                'db_table': 'biz_brands',
            },
        ),
    ]
