# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-21 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0023_auto_20170418_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='duration',
            field=models.DecimalField(blank=True, decimal_places=2, default='0', max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='workday',
            name='duration',
            field=models.DecimalField(blank=True, decimal_places=2, default='0', max_digits=5, null=True),
        ),
    ]
