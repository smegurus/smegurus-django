# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 11:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactPoint',
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
                ('area_served', models.CharField(blank=True, help_text='The geographic area where a service or offered item is provided.', max_length=127, null=True, verbose_name='Area Served')),
                ('contact_type', models.CharField(blank=True, help_text='A person or organization can have different contact points, for different purposes. For example, a sales contact point, a PR contact point and so on. This property is used to specify the kind of contact point.', max_length=127, null=True, verbose_name='Contact Type')),
                ('email', models.EmailField(blank=True, help_text='Email address.', max_length=254, null=True, verbose_name='Email')),
                ('fax_number', models.CharField(blank=True, help_text='The fax number.', max_length=31, null=True, verbose_name='Fax Number')),
                ('product_supported', models.CharField(blank=True, help_text='The product or service this support contact point is related to (such as product support for a particular product line). This can be a specific product or product line (e.g. "iPhone") or a general category of products or services (e.g. "smartphones").', max_length=31, null=True, verbose_name='Product Supported')),
                ('telephone', models.CharField(blank=True, help_text='The telephone number.', max_length=31, null=True, verbose_name='Telephone')),
            ],
            options={
                'db_table': 'biz_contact_points',
                'verbose_name': 'Contact Point',
                'verbose_name_plural': 'Contact Points',
            },
        ),
        migrations.CreateModel(
            name='GeoCoordinate',
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
                ('address', models.CharField(blank=True, help_text='Physical address of the item.', max_length=255, null=True, verbose_name='Address')),
                ('address_country', models.CharField(blank=True, help_text='The country. For example, USA. You can also provide the two-letter <a href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements">ISO 3166-1 alpha-2</a> country code.', max_length=255, null=True, verbose_name='Address Country')),
                ('elevation', models.FloatField(blank=True, default=0.0, help_text='The elevation of a location (<a href="https://en.wikipedia.org/wiki/World_Geodetic_System">WGS 84</a>).', verbose_name='Elevation')),
                ('latitude', models.FloatField(blank=True, default=0.0, help_text='The latitude of a location. For example 37.42242 (<a href="https://en.wikipedia.org/wiki/World_Geodetic_System">WGS 84</a>).', verbose_name='Latitude')),
                ('longitude', models.FloatField(blank=True, default=0.0, help_text='The longitude of a location. For example -122.08585 (<a href="https://en.wikipedia.org/wiki/World_Geodetic_System">WGS 84</a>).', verbose_name='Longitude')),
                ('postal_code', models.CharField(blank=True, help_text='The postal code. For example, 94043.', max_length=127, null=True, verbose_name='Postal Code')),
            ],
            options={
                'db_table': 'biz_geocoordinates',
                'verbose_name': 'GeoCoordinate',
                'verbose_name_plural': 'GeoCoordinates',
            },
        ),
        migrations.CreateModel(
            name='Language',
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
            ],
            options={
                'db_table': 'biz_languages',
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
        migrations.CreateModel(
            name='OpeningHoursSpecification',
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
                ('closes', models.CharField(blank=True, help_text='The closing hour of the place or service on the given day(s) of the week.', max_length=5, null=True, verbose_name='Closes')),
                ('day_of_week', models.CharField(blank=True, help_text='The day of the week for which these opening hours are valid.', max_length=2, null=True, verbose_name='Day Of Week')),
                ('opens', models.CharField(blank=True, help_text='The opening hour of the place or service on the given day(s) of the week.', max_length=5, null=True, verbose_name='Opens')),
                ('valid_from', models.DateField(blank=True, help_text='The date when the item becomes valid.', null=True, verbose_name='Valid From')),
                ('valid_through', models.DateField(blank=True, help_text='The end of the validity of offer, price specification, or opening hours data.', null=True, verbose_name='Valid Through')),
            ],
            options={
                'db_table': 'biz_opening_hours_specifications',
                'verbose_name': 'Opening Hours Specification',
                'verbose_name_plural': 'Opening Hours Specifications',
            },
        ),
        migrations.CreateModel(
            name='PostalAddress',
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
                ('address_country', models.CharField(blank=True, help_text='The country. For example, USA. You can also provide the two-letter <a href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements">ISO 3166-1 alpha-2</a> country code.', max_length=127, null=True, verbose_name='Address Country')),
                ('address_locality', models.CharField(blank=True, help_text='The locality. For example, Mountain View.', max_length=127, null=True, verbose_name='Address Locality')),
                ('address_region', models.CharField(blank=True, help_text='The region. For example, CA.', max_length=127, null=True, verbose_name='Address Region')),
                ('post_office_box_number', models.CharField(blank=True, help_text='The post office box number for PO box addresses.', max_length=127, null=True, verbose_name='Post Office Box Number')),
                ('postal_code', models.CharField(blank=True, help_text='The postal code. For example, 94043.', max_length=127, null=True, verbose_name='Postal Code')),
                ('street_address', models.CharField(blank=True, help_text='The street address. For example, 1600 Amphitheatre Pkwy.', max_length=255, null=True, verbose_name='Street Address')),
            ],
            options={
                'db_table': 'biz_postal_addresses',
                'verbose_name': 'Postal Address',
                'verbose_name_plural': 'Postal Addresses',
            },
        ),
        migrations.CreateModel(
            name='PrivateFileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('datafile', models.FileField(blank=True, help_text='An file of the upload.', null=True, upload_to='upload', verbose_name='File')),
                ('owner', models.ForeignKey(blank=True, help_text='The user whom owns this object.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'biz_private_file_uploads',
                'verbose_name': 'File Upload',
                'verbose_name_plural': 'File Uploads',
            },
        ),
        migrations.CreateModel(
            name='PrivateImageUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('imagefile', models.ImageField(blank=True, help_text='An image of the upload.', null=True, upload_to='upload', verbose_name='Image')),
                ('owner', models.ForeignKey(blank=True, help_text='The user whom owns this object.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'biz_private_image_uploads',
                'verbose_name': 'Image Upload',
                'verbose_name_plural': 'Image Uploads',
            },
        ),
        migrations.AddField(
            model_name='postaladdress',
            name='image',
            field=models.ForeignKey(blank=True, help_text='An image of the item.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thing_image_api_postaladdress_related', to='api.PrivateImageUpload'),
        ),
        migrations.AddField(
            model_name='postaladdress',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='The user whom owns this thing.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='openinghoursspecification',
            name='image',
            field=models.ForeignKey(blank=True, help_text='An image of the item.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thing_image_api_openinghoursspecification_related', to='api.PrivateImageUpload'),
        ),
        migrations.AddField(
            model_name='openinghoursspecification',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='The user whom owns this thing.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='language',
            name='image',
            field=models.ForeignKey(blank=True, help_text='An image of the item.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thing_image_api_language_related', to='api.PrivateImageUpload'),
        ),
        migrations.AddField(
            model_name='language',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='The user whom owns this thing.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='geocoordinate',
            name='image',
            field=models.ForeignKey(blank=True, help_text='An image of the item.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thing_image_api_geocoordinate_related', to='api.PrivateImageUpload'),
        ),
        migrations.AddField(
            model_name='geocoordinate',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='The user whom owns this thing.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='available_language',
            field=models.ForeignKey(blank=True, help_text='A language someone may use with the item.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact_point_available_language', to='api.Language'),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='hours_available',
            field=models.ManyToManyField(blank=True, help_text='The hours during which this service or contact is available.', related_name='contact_point_hours_available', to='api.OpeningHoursSpecification'),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='image',
            field=models.ForeignKey(blank=True, help_text='An image of the item.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thing_image_api_contactpoint_related', to='api.PrivateImageUpload'),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='The user whom owns this thing.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
