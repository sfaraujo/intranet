# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-06 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0015_auto_20161206_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='hours',
        ),
        migrations.AddField(
            model_name='task',
            name='duration',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]