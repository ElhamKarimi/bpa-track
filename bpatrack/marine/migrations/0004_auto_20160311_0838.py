# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-11 00:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marine', '0003_contextualpelagic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contextualpelagic',
            old_name='condictivity',
            new_name='conductivity',
        ),
    ]