# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-13 04:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='site',
            old_name='location_description',
            new_name='name',
        ),
    ]
