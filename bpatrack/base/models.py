# -*- coding: utf-8 -*-
from django.db import models
from bpatrack.users.models import User
from bpatrack.common.models import (
        Facility,
        Amplicon,
        Metagenomic,
        DataSet,
        )

class DataSet(DataSet):
    project = "BASE"

class TransferLog(models.Model):
    """ Notes transfer of a dataset to the archive """

    facility = models.ForeignKey(Facility)
    transfer_to_facility_date = models.DateField("Transfer to Facility Date")
    description = models.CharField("Description", max_length=100)
    data_type = models.CharField("Data Type", max_length=50)
    folder_name = models.CharField("Folder", max_length=100)

    dataset = models.ForeignKey(DataSet)

    class Meta:
        verbose_name = 'Transfer Log'
        verbose_name_plural = 'Transfers'

    def __str__(self):
        return "{} {}".format(self.facility, self.description)


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


