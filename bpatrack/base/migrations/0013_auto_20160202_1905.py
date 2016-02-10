# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-02 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_auto_20160202_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amplicon',
            name='metadata_filename',
            field=models.CharField(max_length=100, verbose_name='Metadata Filename'),
        ),
        migrations.AlterField(
            model_name='metagenomic',
            name='metadata_filename',
            field=models.CharField(max_length=100, verbose_name='Metadata Filename'),
        ),
    ]