# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-12 07:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Facility short name', max_length=100, unique=True, verbose_name='Facility Name')),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Facilities',
            },
        ),
    ]
