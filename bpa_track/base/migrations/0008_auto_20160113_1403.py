# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-13 06:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20160113_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amplicon',
            name='sequencing_facility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facility', to='common.Facility', verbose_name='Sequencing Facility'),
        ),
    ]