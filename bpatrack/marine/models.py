# -*- coding: utf-8 -*-
from django.db import models
from bpatrack.users.models import User
from bpatrack.common.models import (
        Facility,
        TransferLog,
        Amplicon,
        Metagenomic,
        )

class TransferLog(TransferLog):
    pass

class Metagenomic(Metagenomic):
    pass

class Amplicon(Amplicon):
    pass

class SampleStateTrack(models.Model):

    extraction_id = models.CharField(
            'Sample Extraction ID',
            max_length=100,
            primary_key=True)

    quality_check_preformed = models.BooleanField("Quality Checked", default=False)
    metagenomics_data_generated = models.BooleanField("Metagenomics Data Generated", default=False)
    amplicon_16s_data_generated = models.BooleanField("Amplicon 16S Data Generated", default=False)
    amplicon_18s_data_generated = models.BooleanField("Amplicon 18S Data Generated", default=False)
    amplicon_ITS_data_generated = models.BooleanField("Amplicon ITS Data Generated", default=False)
    minimum_contextual_data_received = models.BooleanField("Minimum Contextual Data Received", default=False)
    full_contextual_data_received = models.BooleanField("Full Contextual Data Received", default=False)

    class Meta:
        verbose_name = 'Sample State Track Log'

    def __str__(self):
        return "{}" .format( self.extraction_id)
