from django.db import models
from bpa_datatracker.users.models import User

class SampleReceived(models.Model):
    """ Notes the reception of a sample at a Vendor """

    VENDORS = (
           ("AGRF", "Australian Genome Research Facility (AGRF)"),
           ("RAM", "Ramaciotti Centre for Genomics"),
           )

    vendor = models.CharField(max_length=5, choices=VENDORS, null=True)
    extraction_id = models.CharField(max_length=12, primary_key=True)
    batch_number = models.CharField(max_length=20)
    date_received = models.DateField()
    submitter = models.ForeignKey(User, null=True)

    def __str__(self):
        return "{} {} received at {}".format(self.extraction_id, self.batch_number, self.date_received)

    class Meta:
        verbose_name = 'Sample Received'
        verbose_name_plural = 'Samples Received'
