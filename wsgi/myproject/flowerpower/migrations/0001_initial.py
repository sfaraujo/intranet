# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-13 13:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Evapotranspiration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('air_temperature', models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True)),
                ('air_temperature_text', models.CharField(blank=True, max_length=255)),
                ('battery', models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True)),
                ('fertilizer', models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True)),
                ('fertilizer_text', models.CharField(blank=True, max_length=255)),
                ('fertilizer_last_sample', models.DateTimeField(blank=True, null=True)),
                ('light', models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True)),
                ('light_text', models.CharField(blank=True, max_length=255)),
                ('total_samples_count', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status_creation_datetime_utc', models.DateTimeField(blank=True, null=True)),
                ('last_sample_utc', models.DateTimeField(blank=True, null=True)),
                ('last_sample_upload', models.DateTimeField(blank=True, null=True)),
                ('soil_moisture', models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True)),
                ('soil_moisture_text', models.CharField(blank=True, max_length=255)),
                ('avatar_url', models.CharField(blank=True, max_length=255)),
                ('latitude', models.CharField(blank=True, max_length=255)),
                ('longitude', models.CharField(blank=True, max_length=255)),
                ('location_identifier', models.CharField(blank=True, max_length=255)),
                ('sensor_serial', models.CharField(blank=True, max_length=255)),
                ('plant_nickname', models.CharField(blank=True, max_length=255)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='ParrotAuth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('client_id', models.CharField(max_length=255)),
                ('client_secret', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('air_temperature_celsius', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('battery_percent', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('capture_datetime_utc', models.DateTimeField(null=True)),
                ('fertilizer_level', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('light', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('soil_moisture_percent', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sensor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='flowerpower.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_serial', models.CharField(max_length=255)),
                ('plantnickname', models.CharField(blank=True, max_length=255)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
        ),
    ]
