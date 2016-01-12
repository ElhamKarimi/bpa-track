from django.db import models

class Facility(models.Model):
    """ The Sequencing Facility """

    facilities = {'RAM': 'Ramaciotti',
                  'AGRF': 'AGRF'}

    name = models.CharField('Facility Name', max_length=100, help_text='Facility short name', unique=True)
    note = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Facilities'

    def get_name(self, key):
        """ Facilities are commonly known by theses names, return standard name. """

        try:
            return self.facilities[key]
        except KeyError:
            return 'Unknown'

    def __str__(self):
        return u'{0}'.format(self.name)
