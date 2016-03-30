# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-30 03:12
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0012_auto_20160329_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='location_description',
            field=models.TextField(verbose_name='Location Description'),
        ),
        migrations.AlterField(
            model_name='site',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(help_text='Represented as (longitude, latitude)', primary_key=True, serialize=False, srid=4326, verbose_name='Position'),
        ),
    ]
