# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-06 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_auto_20161206_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='hours',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
