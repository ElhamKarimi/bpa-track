# -*- coding: utf-8 -*-
from django.db import models
from bpa_datatracker.users.models import User
from bpa_datatracker.common.models import Facility


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


class Amplicon(models.Model):
    """ BASE Amplicon Soil Sample """

    TYPES = (
            ('16S', '16S'),
            ('ITS', 'ITS'),
            ('18S', '18S'),
            ('A16S', 'A16S')
            )

    sample_extraction_id = models.CharField(
            'Sample Extraction ID',
            max_length=100,
            blank=True,
            null=True)

    sequencing_facility = models.ForeignKey(Facility,
                                            verbose_name='Sequencing Facility',
                                            related_name='facility',
                                            blank=True,
                                            null=True)

    target = models.CharField(
            'Type',
            max_length=4,
            choices=TYPES)

    comments = models.TextField('Comments', blank=True, null=True)

    def __str__(self):
        return u'{0}:{1}:{2}'.format(self.sample_extraction_id, self.sequencing_facility, self.target)

    class Meta:
        verbose_name_plural = 'Amplicon Sequences'
