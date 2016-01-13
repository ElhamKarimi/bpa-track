from django.db import models

class Facility(models.Model):
    """ The Sequencing Facility """

    name = models.CharField('Facility Name', max_length=10, primary_key=True)
    description = models.CharField('Description', max_length=100, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return u'{0}'.format(self.name)
