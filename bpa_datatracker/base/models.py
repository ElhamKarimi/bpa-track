from django.db import models
from bpa_datatracker.users.models import User

class SampleReception(models.Model):
    """ Notes the reception of a sample at a Vendor """

    VENDORS = (
           ("AGRF", "Australian Genome Research Facility (AGRF)"),
           ("RAM", "Ramaciotti Centre for Genomics"),
           )

    vendor = models.CharField(max_length=5, choices=VENDORS)
    extraction_id = models.CharField(max_length=12)
    batch_number = models.CharField(max_length=20)
    date_received = models.DateField()
    submitter = User()

