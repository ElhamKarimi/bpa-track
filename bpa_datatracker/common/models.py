from django.db import models

class Facility(models.Model):
    """ The Sequencing Facility """

    FACILITIES = (('RAM',' Ramaciotti'),
                  ('AGRF', 'AGRF'))

    name = models.CharField('Facility Name', max_length=4, choices=FACILITIES, primary_key=True)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return u'{0}'.format(self.name)
