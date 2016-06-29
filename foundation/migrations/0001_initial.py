# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 13:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_tenants.postgresql_backend.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BannedDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=63, unique=True)),
                ('banned_on', models.DateField(auto_now_add=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=127, null=True)),
            ],
            options={
                'db_table': 'biz_banned_domains',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='BannedIP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.GenericIPAddressField(db_index=True, unique=True)),
                ('banned_on', models.DateField(auto_now_add=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=127, null=True)),
            ],
            options={
                'db_table': 'biz_banned_ips',
                'ordering': ('address',),
            },
        ),
        migrations.CreateModel(
            name='BannedWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(db_index=True, max_length=63, unique=True)),
                ('banned_on', models.DateField(auto_now_add=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=127, null=True)),
            ],
            options={
                'db_table': 'biz_banned_words',
                'ordering': ('text',),
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(max_length=63, unique=True, validators=[django_tenants.postgresql_backend.base._check_schema_name])),
                ('name', models.CharField(max_length=100)),
                ('paid_until', models.DateField(auto_now_add=True, null=True)),
                ('on_trial', models.BooleanField(default=False)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicFileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('datafile', models.FileField(blank=True, help_text='An file of the upload.', null=True, upload_to='upload', verbose_name='File')),
                ('owner', models.ForeignKey(blank=True, help_text='The user whom owns this object.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'File Upload',
                'verbose_name_plural': 'File Uploads',
                'db_table': 'biz_public_file_uploads',
            },
        ),
        migrations.CreateModel(
            name='PublicImageUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('imagefile', models.ImageField(blank=True, help_text='An image of the upload.', null=True, upload_to='upload', verbose_name='Image')),
                ('owner', models.ForeignKey(blank=True, help_text='The user whom owns this object.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Image Upload',
                'verbose_name_plural': 'Image Uploads',
                'db_table': 'biz_public_image_uploads',
            },
        ),
        migrations.AddField(
            model_name='domain',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='foundation.Organization'),
        ),
    ]
