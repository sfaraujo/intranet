# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-09 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowerpower', '0003_auto_20161114_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='battery',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True),
        ),
    ]
