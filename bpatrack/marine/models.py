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

class SampleStateTrack(models.Model):

    extraction_id = models.CharField(
            'Sample Extraction ID',
            max_length=100,
            primary_key=True)

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

class ContextualPelagic(models.Model):
    
    #BPA_ID
    bpa_id = models.IntegerField('BPA ID', primary_key=True)
    #Date sampled (Y-M-D)
    date_sampled = models.DateField("Date Sampled")
    #Time sampled (hh:mm)
    time_sampled = models.TimeField("Time Sampled")
    # replace with geodjango
    #lat (decimal degrees)
    lat = models.DecimalField("Latitude", max_digits=9, decimal_places=6)
    #long (decimal degrees)
    lon = models.DecimalField("Longitude", max_digits=9, decimal_places=6)
    #Depth (m)
    dept = models.IntegerField('Depth')
    #Location description
    location_description = models.TextField("Location Description", blank=True)
    #Notes
    note = models.TextField("Note", blank=True)
    #Host Species
    note = models.TextField("Host Species", blank=True)
    #pH Level (H2O) (pH)
    ph = models.IntegerField("pH Level H20")
    #Oxygen (μmol/L) Lab
    oxygen = models.IntegerField("Oxygen (μmol/L) Lab")
    #Oxygen (ml/L) CTD
    oxygen_ctd = models.IntegerField("Oxygen (ml/L) CDT")
    #Nitrate/Nitrite (μmol/L)
    nitrate = models.IntegerField("Nitrate/Nitrite (μmol/L)")
    #Phosphate (μmol/L)
    phosphate = models.IntegerField("Phosphate (μmol/L)")
    #Ammonium (μmol/L)
    ammonium = models.IntegerField("Ammonium (μmol/L)")
    #Total CO2 (μmol/kg)
    co2_total = models.IntegerField("Total CO2 (μmol/kg)")
    #Total alkalinity (μmol/kg)
    alkalinity_total = models.IntegerField("Total alkalinity (μmol/kg)")
    #Temperature [ITS-90, deg C]
    temperature = models.IntegerField("Temperature [ITS-90, deg C]")
    #Conductivity [S/m]
    conductivity = models.IntegerField("Conductivity [S/m]")
    #Turbidity (Upoly 0, WET Labs FLNTURT)
    turbitity = models.IntegerField("Turbidity (Upoly 0, WET Labs FLNTURT)")
    #Salinity [PSU] Laboratory
    salinity = models.IntegerField("Salinity [PSU] Laboratory")
    #microbial abundance (cells per ml)
    microbial_abandance = models.IntegerField("Microbial abundance (cells per ml)")
    #chlorophyll a (μg/L)
    chlorophyl = models.IntegerField("Chlorophyll a (μg/L)")
    #%total carbon
    carbon_total = models.IntegerField("% total carbon")
    #% total inorganc carbon
    inorganic_carbon_total = models.IntegerField("% total inorganc carbon")
    #light intensity (lux)
    flux = models.IntegerField("Light intensity (lux)")

    class Meta:
        verbose_name = 'Pelagic marine Contextual Data'

    def __str__(self):
        return "{} Pelagic Contextual Data" .format( self.extraction_id)
