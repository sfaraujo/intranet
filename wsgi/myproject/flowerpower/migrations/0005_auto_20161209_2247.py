# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-09 22:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowerpower', '0004_auto_20161209_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='light',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True),
        ),
    ]