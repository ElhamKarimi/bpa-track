from django.contrib.gis.db import models
from autoslug import AutoSlugField

class Site(models.Model):
    """ A site """

    point = models.PointField("Position", help_text="Represented as (longitude, latitude)")
    #Depth (m)
    depth = models.IntegerField('Depth')
    # Notes
    note = models.TextField("Note", null=True, blank=True)
    # Location description
    location_description = models.TextField("Location Description")

    slug = AutoSlugField(populate_from='point', unique=True, max_length=255)


    def __str__(self):
        return '{} {}'.format(self.point, self.location_description)

class Facility(models.Model):
    """ The Sequencing Facility """

    name = models.CharField('Facility Name', max_length=10, primary_key=True)
    description = models.CharField('Description', max_length=100, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return '{0}'.format(self.name)


class DataSet(models.Model):
    """ Model representing a dataset """

    name = models.CharField('Dataset', max_length=20, primary_key=True)
    transfer_to_archive_date = models.DateField("Transfer to Archive Date")
    facility = models.ForeignKey(
            Facility,
            related_name='%(app_label)s_%(class)s_facility',
            verbose_name='Sequencing Facility',
            blank=True,
            null=True)

    ticket_url = models.URLField('JIRA')
    downloads_url = models.URLField('Downloads')
    note = models.TextField("Note", blank=True)

    class Meta:
        abstract = True
        verbose_name_plural = 'Datasets'

    def __str__(self):
        return '{}'.format(self.name)


class TransferLog(models.Model):
    """ Notes transfer to CCG """

    facility = models.ForeignKey(
            Facility,
            related_name='%(app_label)s_%(class)s_facility',
            verbose_name='Sequencing Facility',
            blank=True,
            null=True)
    transfer_to_facility_date = models.DateField("Transfer to Facility Date")
    description = models.CharField("Description", max_length=100)
    data_type = models.CharField("Data Type", max_length=50)
    folder_name = models.CharField("Folder", max_length=100)
    transfer_to_archive_date = models.DateField("Transfer to Archive Date")
    notes = models.TextField('Notes', blank=True, null=True)

    ticket_url = models.URLField('Dataset')
    downloads_url = models.URLField('Downloads')

    class Meta:
        abstract = True
        verbose_name = 'Transfer Log'
        verbose_name_plural = 'Transfers'

    def __str__(self):
        return "{} {}".format(self.facility, self.description)


class Amplicon(models.Model):
    """ BASE Amplicon Soil Sample """

    TYPES = (
            ('16S', '16S'),
            ('ITS', 'ITS'),
            ('18S', '18S'),
            ('A16S', 'A16S')
            )

    extraction_id = models.CharField(
            'Sample Extraction ID',
            max_length=100,
            blank=True,
            null=True)

    facility = models.ForeignKey(
            Facility,
            related_name='%(app_label)s_%(class)s_facility',
            verbose_name='Sequencing Facility',
            blank=True,
            null=True)

    target = models.CharField(
            'Type',
            max_length=4,
            choices=TYPES)

    metadata_filename = models.CharField('Metadata Filename', max_length=100)

    comments = models.TextField('Comments', blank=True, null=True)

    def __str__(self):
        return u'{0}:{1}:{2}'.format(self.extraction_id, self.facility, self.target)

    class Meta:
        abstract = True
        verbose_name_plural = 'Amplicon Sequences'


class Metagenomic(models.Model):
    """ Metagenomic  """

    extraction_id = models.CharField(
            'Sample Extraction ID',
            max_length=100,
            blank=True,
            null=True)

    facility = models.ForeignKey(
            Facility,
            related_name='%(app_label)s_%(class)s_facility',
            verbose_name='Sequencing Facility',
            blank=True,
            null=True)

    metadata_filename = models.CharField('Metadata Filename', max_length=100)

    comments = models.TextField('Comments', blank=True, null=True)

    def __str__(self):
        return u'{0}:{1}'.format(self.extraction_id, self.facility)

    class Meta:
        abstract = True
        verbose_name_plural = 'Metagenomic Sequences'
