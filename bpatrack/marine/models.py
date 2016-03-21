from django.db import models
from bpatrack.users.models import User
from bpatrack.common.models import (
        Facility,
        TransferLog,
        Amplicon,
        Metagenomic,
        )


class MarineCommon(models.Model):
    """ Marine Common """
    
    sample_type = "UNSET"
    # BPA_ID
    bpa_id = models.IntegerField('BPA ID', primary_key=True)
    # Date sampled (Y-M-D)
    date_sampled = models.DateField("Date Sampled")
    # Time sampled (hh:mm)
    time_sampled = models.TimeField("Time Sampled")
    #lat (decimal degrees)
    lat = models.DecimalField("Latitude", max_digits=9, decimal_places=6)
    #long (decimal degrees)
    lon = models.DecimalField("Longitude", max_digits=9, decimal_places=6)
    #Depth (m)
    dept = models.IntegerField('Depth')
    # Notes
    note = models.TextField("Note", null=True, blank=True)
    # Location description
    location_description = models.TextField("Location Description")

    class Meta:
        abstract = True

    def __str__(self):
        return "{} {}".format(self.extraction_id, self.sample_type)

class TransferLog(TransferLog):
    pass

class Metagenomic(Metagenomic):
    pass

class Amplicon(Amplicon):
    pass

class SampleStateTrack(models.Model):

    extraction_id = models.CharField( 'Sample Extraction ID', max_length=100, primary_key=True)
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

class ContextualPelagic(MarineCommon):
    """ Pelagic """

    sample_type = "Pelagic"

    #Host Species
    host_species = models.TextField("Host Species", null=True, blank=True)
    #pH Level (H2O) (pH)
    ph = models.IntegerField("pH Level H20", null=True, blank=True)
    #Oxygen (μmol/L) Lab
    oxygen = models.IntegerField("Oxygen (μmol/L) Lab", null=True, blank=True)
    #Oxygen (ml/L) CTD
    oxygen_ctd = models.IntegerField("Oxygen (ml/L) CDT", null=True, blank=True)
    #Nitrate/Nitrite (μmol/L)
    nitrate = models.IntegerField("Nitrate/Nitrite (μmol/L)", null=True, blank=True)
    #Phosphate (μmol/L)
    phosphate = models.IntegerField("Phosphate (μmol/L)", null=True, blank=True)
    #Ammonium (μmol/L)
    ammonium = models.IntegerField("Ammonium (μmol/L)", null=True, blank=True)
    #Total CO2 (μmol/kg)
    co2_total = models.IntegerField("Total CO2 (μmol/kg)", null=True, blank=True)
    #Total alkalinity (μmol/kg)
    alkalinity_total = models.IntegerField("Total alkalinity (μmol/kg)", null=True, blank=True)
    #Temperature [ITS-90, deg C]
    temperature = models.IntegerField("Temperature [ITS-90, deg C]", null=True, blank=True)
    #Conductivity [S/m]
    conductivity = models.IntegerField("Conductivity [S/m]", null=True, blank=True)
    #Turbidity (Upoly 0, WET Labs FLNTURT)
    turbitity = models.IntegerField("Turbidity (Upoly 0, WET Labs FLNTURT)", null=True, blank=True)
    #Salinity [PSU] Laboratory
    salinity = models.IntegerField("Salinity [PSU] Laboratory", null=True, blank=True)
    #microbial abundance (cells per ml)
    microbial_abandance = models.IntegerField("Microbial abundance (cells per ml)", null=True, blank=True)
    #chlorophyll a (μg/L)
    chlorophyl = models.IntegerField("Chlorophyll a (μg/L)", null=True, blank=True)
    #%total carbon
    carbon_total = models.IntegerField("% total carbon", null=True, blank=True)
    #% total inorganc carbon
    inorganic_carbon_total = models.IntegerField("% total inorganc carbon", null=True, blank=True)
    #light intensity (lux)
    flux = models.IntegerField("Light intensity (lux)", null=True, blank=True)

    class Meta:
        verbose_name = 'Pelagic marine Contextual Data'

    def __str__(self):
        return "{} Pelagic Contextual Data".format( self.bpa_id)

class CoralWeedGrassCommon(MarineCommon):

    # Pulse amplitude modulated (PAM)
    pam = models.DecimalField("Pulse amplitude modulated (PAM)")
    # fluorometer measurement
    fluoro = models.DecimalField("Fluorometer Measurement")
    # host state (free text field)
    host_state = models.TextField("Host State")
    # host abundance (individuals per m2)
    host_abundance = models.DecimalField("Fluorometer Measurement")

    class Meta(MarineCommon.Meta):
        abstract = True

class SeaWeed(CoralWeedGrassCommon):
    """ Seaweed """
    sample_type = "SeaWeed"

class SeaGrass(CoralWeedGrassCommon):
    """ SeaGrass """
    sample_type = "SeaGrass"

class Coral(CoralWeedGrassCommon):
    """ Coral"""
    sample_type = "Coral"

