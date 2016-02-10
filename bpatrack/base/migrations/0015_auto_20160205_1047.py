# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 02:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_transferlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amplicon',
            name='facility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='base_amplicon_facility', to='common.Facility', verbose_name='Sequencing Facility'),
        ),
        migrations.AlterField(
            model_name='metagenomic',
            name='facility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='base_metagenomic_facility', to='common.Facility', verbose_name='Sequencing Facility'),
        ),
        migrations.AlterField(
            model_name='transferlog',
            name='facility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='base_transferlog_facility', to='common.Facility', verbose_name='Sequencing Facility'),
        ),
    ]