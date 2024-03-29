# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-13 02:22
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('name', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Facility Name')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='Description')),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Facilities',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_description', models.TextField(unique=True, verbose_name='Location Description')),
                ('point', django.contrib.gis.db.models.fields.PointField(help_text='Represented as (longitude, latitude)', srid=4326, verbose_name='Position')),
                ('note', models.TextField(blank=True, null=True, verbose_name='Note')),
            ],
            options={
                'verbose_name_plural': 'Sample Sites',
                'verbose_name': 'Sample Site',
            },
        ),
    ]
