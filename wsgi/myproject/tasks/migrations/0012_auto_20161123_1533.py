# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-23 15:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0011_auto_20161121_1658'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='end_date',
            new_name='endDate',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='start_date',
            new_name='startDate',
        ),
    ]
