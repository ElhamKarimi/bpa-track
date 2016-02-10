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

class SampleReceived(models.Model):
    """ Notes the reception of a sample at a Vendor """

    extraction_id = models.CharField(max_length=12, primary_key=True)
    batch_number = models.CharField(max_length=20)
    date_received = models.DateField()
    submitter = models.ForeignKey(User, null=True)

    facility = models.ForeignKey(
            Facility,
            verbose_name='Sequencing Facility',
            blank=True,
            null=True)

    def __str__(self):
        return "{} {} received at {}".format(self.extraction_id, self.batch_number, self.date_received)

    class Meta:
        verbose_name = 'Sample Received'
        verbose_name_plural = 'Samples Received'


