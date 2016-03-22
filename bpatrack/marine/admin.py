from dateutil.parser import parse as date_parser
from django.contrib import admin
from django.utils.html import format_html
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from bpatrack.users.models import User
from bpatrack.users.admin import UserWidget

from bpatrack.common.models import Facility
from bpatrack.common.admin import (
        FacilityWidget,
        DateField,
        CommonAmpliconResource,
        CommonAmpliconAdmin,
        CommonMetagenomicResource,
        CommonMetagenomicAdmin,
        CommonTransferLogResource,
        CommonTransferLogAdmin,
        )

from .models import (
        Amplicon,
        Metagenomic,
        TransferLog,
        SampleStateTrack,
        ContextualPelagic,
        ContextualOpenWater,
        SeaWeed,
        SeaGrass,
        Coral,
        Sediment,
        Sponge,
        )


# TransferLog
class TransferLogResource(CommonTransferLogResource):
    class Meta(CommonTransferLogResource.Meta):
        model = TransferLog


class TransferLogAdmin(CommonTransferLogAdmin):
    resource_class = TransferLogResource


# Amplicon
class AmpliconResource(CommonAmpliconResource):
    class Meta(CommonAmpliconResource.Meta):
        model = Amplicon


class AmpliconAdmin(CommonAmpliconAdmin):
    resource_class = AmpliconResource


# Metagenomic
class MetagenomicResource(CommonMetagenomicResource):
    class Meta(CommonMetagenomicResource.Meta):
        model = Metagenomic


class MetagenomicAdmin(CommonMetagenomicAdmin):
    resource_class = MetagenomicResource


class SampleStateTrackAdmin(ImportExportModelAdmin):
    list_display = (
            'extraction_id',
            'quality_check_preformed',
            'metagenomics_data_generated',
            'amplicon_16s_data_generated',
            'amplicon_18s_data_generated',
            'amplicon_ITS_data_generated',
            'minimum_contextual_data_received',
            'full_contextual_data_received'
            )

    list_filter = (
            'quality_check_preformed',
            'metagenomics_data_generated',
            'amplicon_16s_data_generated',
            'amplicon_18s_data_generated',
            'amplicon_ITS_data_generated',
            'minimum_contextual_data_received',
            'full_contextual_data_received'
            )


# Pelagic
class ContextualPelagicResource(resources.ModelResource):

    bpa_id = fields.Field(attribute="bpa_id", column_name="BPA_ID")
    date_sampled = DateField(attribute="date_sampled", column_name="Date Sampled")
    time_sampled = DateField(attribute="time_sampled", column_name="Time Sampled")
    lat = fields.Field(attribute="lat", column_name="Latitude")
    lon = fields.Field(attribute="lon", column_name="Longitude")
    dept = fields.Field(attribute="dept", column_name="Dept")
    location_description = fields.Field(attribute="location_description", column_name="Location Description")
    note = fields.Field(attribute="note", column_name="Note")
    host_species = fields.Field(attribute="host_species", column_name="Host Species")
    ph = fields.Field(attribute="ph", column_name="pH Level H20")
    oxygen = fields.Field(attribute="oxygen", column_name="Oxygen (μmol/L) Lab")
    oxygen_ctd = fields.Field(attribute="oxygen_ctd", column_name="Oxygen (ml/L) CDT")
    nitrate = fields.Field(attribute="nitrate", column_name="Nitrate/Nitrite (μmol/L)")
    phosphate = fields.Field(attribute="phosphate", column_name="Phosphate (μmol/L)")
    ammonium = fields.Field(attribute="ammonium", column_name="Ammonium (μmol/L)")
    co2_total = fields.Field(attribute="co2_total", column_name="Total CO2 (μmol/kg)")
    alkalinity_total = fields.Field(attribute="alkalinity_total", column_name="Total alkalinity (μmol/kg)")
    temperature = fields.Field(attribute="temperature", column_name="Temperature [ITS-90, deg C]")
    conductivity = fields.Field(attribute="conductivity", column_name="Conductivity [S/m]")
    turbitity = fields.Field(attribute="turbitity", column_name="Turbidity (Upoly 0, WET Labs FLNTURT)")
    salinity = fields.Field(attribute="salinity", column_name="Salinity [PSU] Laboratory")
    microbial_abandance = fields.Field(attribute="microbial_abundance", column_name="Microbial abundance (cells per ml)")
    chlorophyl = fields.Field(attribute="chlorophyl", column_name="Chlorophyll a (μg/L)")
    carbon_total = fields.Field(attribute="carbon_total", column_name="% total carbon")
    inorganic_carbon_total = fields.Field(attribute="inorganic_carbon_total", column_name="% total inorganc carbon")
    flux = fields.Field(attribute="flux", column_name="Light intensity (lux)")

    class Meta:
        model = ContextualPelagic
        import_id_fields = ('bpa_id', )


class ContextualPelagicAdmin(ImportExportModelAdmin):
    resource_class = ContextualPelagicResource
    list_display = (
            'bpa_id',
            'date_sampled',
            'location_description',
            )

    _required = (
            'bpa_id',
            'date_sampled',
            'time_sampled',
            'lat',
            'lon',
            'dept',
            'location_description',
            'host_species',
            )

    _extra = (
            'ph',
            'oxygen',
            'oxygen_ctd',
            'nitrate',
            'phosphate',
            'ammonium',
            'co2_total',
            'alkalinity_total',
            'temperature',
            'conductivity',
            'turbitity',
            'salinity',
            'microbial_abandance',
            'chlorophyl',
            'carbon_total',
            'inorganic_carbon_total',
            'flux',
            'note',
            )

    fieldsets = (
            (None, {
                'fields': _required,
                }),
            ('Detailed Contextual', {
                'classes': ('collapse',),
                'fields': _extra,
                }),
            )


# Open Water
class ContextualOpenWaterResource(resources.ModelResource):

    bpa_id = fields.Field(attribute="bpa_id", column_name="BPA_ID")
    date_sampled = DateField(attribute="date_sampled", column_name="Date Sampled")
    time_sampled = DateField(attribute="time_sampled", column_name="Time Sampled")
    lat = fields.Field(attribute="lat", column_name="Latitude")
    lon = fields.Field(attribute="lon", column_name="Longitude")
    dept = fields.Field(attribute="dept", column_name="Dept")
    location_description = fields.Field(attribute="location_description", column_name="Location Description")
    note = fields.Field(attribute="note", column_name="Note")
    host_species = fields.Field(attribute="host_species", column_name="Host Species")
    ph = fields.Field(attribute="ph", column_name="pH Level H20")
    oxygen = fields.Field(attribute="oxygen", column_name="Oxygen (μmol/L) Lab")
    oxygen_ctd = fields.Field(attribute="oxygen_ctd", column_name="Oxygen (ml/L) CDT")
    nitrate = fields.Field(attribute="nitrate", column_name="Nitrate/Nitrite (μmol/L)")
    phosphate = fields.Field(attribute="phosphate", column_name="Phosphate (μmol/L)")
    ammonium = fields.Field(attribute="ammonium", column_name="Ammonium (μmol/L)")
    co2_total = fields.Field(attribute="co2_total", column_name="Total CO2 (μmol/kg)")
    alkalinity_total = fields.Field(attribute="alkalinity_total", column_name="Total alkalinity (μmol/kg)")
    temperature = fields.Field(attribute="temperature", column_name="Temperature [ITS-90, deg C]")
    conductivity = fields.Field(attribute="conductivity", column_name="Conductivity [S/m]")
    turbitity = fields.Field(attribute="turbitity", column_name="Turbidity (Upoly 0, WET Labs FLNTURT)")
    salinity = fields.Field(attribute="salinity", column_name="Salinity [PSU] Laboratory")
    microbial_abandance = fields.Field(attribute="microbial_abundance", column_name="Microbial abundance (cells per ml)")
    chlorophyl = fields.Field(attribute="chlorophyl", column_name="Chlorophyll a (μg/L)")
    carbon_total = fields.Field(attribute="carbon_total", column_name="% total carbon")
    inorganic_carbon_total = fields.Field(attribute="inorganic_carbon_total", column_name="% total inorganc carbon")
    flux = fields.Field(attribute="flux", column_name="Light intensity (lux)")

    class Meta:
        model = ContextualOpenWater
        import_id_fields = ('bpa_id', )


class ContextualOpenWaterAdmin(ImportExportModelAdmin):
    resource_class = ContextualOpenWaterResource

    list_display = (
            'bpa_id',
            'date_sampled',
            'location_description',
            )

    _required = (
            'bpa_id',
            'date_sampled',
            'time_sampled',
            'lat',
            'lon',
            'dept',
            'location_description',
            'host_species',
            )

    _extra = (
            'ph',
            'oxygen',
            'oxygen_ctd',
            'silicate',
            'nitrate',
            'fluorescence',
            'tss',
            'inorganic_fraction',
            'biomass',
            'allo',
            'alpha_beta_car',
            'nth',
            'asta',
            'beta_beta_car',
            'beta_epi_car',
            'but_fuco',
            'cantha',
            'cphl_a',
            'cphl_b',
            'cphl_c1c2',
            'cphl_c1',
            'cphl_c2',
            'cphl_c3',
            'cphlide_a',
            'diadchr',
            'diadino',
            'diato',
            'dino',
            'dv_cphl_a_and_cphl_a',
            'dv_cphl_a',
            'dv_cphl_b_and_cphl_b',
            'dv_cphl_b',
            'echin',
            'fuco',
            'gyro',
            'hex_fuco',
            'keto_hex_fuco',
            'lut',
            'lyco',
            'mg_dvp',
            'neo',
            'perid',
            'phide_a',
            'phytin_a',
            'phytin_b',
            'pras',
            'pyrophide_a',
            'pyrophytin_a',
            'viola',
            'zea',
            )

    fieldsets = (
            (None, {
                'fields': _required,
                }),
            ('Detailed Contextual', {
                'classes': ('collapse',),
                'fields': _extra,
                }),
            )


class MarineResource(resources.ModelResource):
    """ SeaWeed, Coral and SeaGrass common resource """

    bpa_id = fields.Field(attribute="bpa_id", column_name="BPA_ID")
    date_sampled = DateField(attribute="date_sampled", column_name="Date Sampled")
    time_sampled = DateField(attribute="time_sampled", column_name="Time Sampled")
    lat = fields.Field(attribute="lat", column_name="Latitude")
    lon = fields.Field(attribute="lon", column_name="Longitude")
    dept = fields.Field(attribute="dept", column_name="Dept")
    location_description = fields.Field(attribute="location_description", column_name="Location Description")
    note = fields.Field(attribute="note", column_name="Note")
    host_species = fields.Field(attribute="host_species", column_name="Host Species")

    class Meta:
        import_id_fields = ('bpa_id', )


# sediment
class SedimentResource(MarineResource):

    carbon = fields.Field(attribute="carbon", column_name="% total carbon")
    sediment = fields.Field(attribute="sediment", column_name="% fine sediment")
    nitrogen = fields.Field(attribute="nitrogen", column_name="% total nitrogen")
    phosphorous = fields.Field(attribute="phosphorous", column_name="% total phosphorous")
    sedimentation_rate = fields.Field(attribute="sedimentation_rate", column_name="sedimentation rate (g /(cm2 x y)r)")


class SpongeResource(MarineResource):

    host_state = fields.Field(attribute="host_state", column_name="host state (free text field)")
    host_abundance = fields.Field(attribute="host_abundance", column_name="host abundance (individuals per m2)")


class CommonResource(MarineResource):
    """ SeaWeed, Coral and SeaGrass common resource """

    pam = fields.Field(attribute="pam", column_name="Pulse amplitude modulated (PAM)")
    fluoro = fields.Field(attribute="fluoro", column_name="Fluorometer Measurement")
    host_state = fields.Field(attribute="host_state", column_name="Host State")
    host_abundance = fields.Field(attribute="host_abundance", column_name="Host Abundance")


class CoralResource(CommonResource):
    class Meta(CommonResource.Meta):
        model = Coral


class SeaGrassResource(CommonResource):
    class Meta(CommonResource.Meta):
        model = SeaGrass


class SeaWeedResource(CommonResource):
    class Meta(CommonResource.Meta):
        model = SeaWeed


class CommonAdmin(ImportExportModelAdmin):
    list_display = (
            'bpa_id',
            'date_sampled',
            'time_sampled',
            'lat',
            'lon',
            )

    list_filter = (
            'bpa_id',
            'date_sampled',
            'time_sampled',
            'lat',
            'lon',
            'dept'
            )


class SedimentAdmin(CommonAdmin):
    resource_class = SedimentResource


class SpongeAdmin(CommonAdmin):
    resource_class = SpongeResource


class CoralAdmin(CommonAdmin):
    resource_class = CoralResource


class SeaWeedAdmin(CommonAdmin):
    resource_class = SeaWeedResource


class SeaGrassAdmin(CommonAdmin):
    resource_class = SeaGrassResource


admin.site.register(Amplicon, AmpliconAdmin)
admin.site.register(Metagenomic, MetagenomicAdmin)
admin.site.register(TransferLog, TransferLogAdmin)
admin.site.register(SampleStateTrack, SampleStateTrackAdmin)
admin.site.register(ContextualPelagic, ContextualPelagicAdmin)
admin.site.register(ContextualOpenWater, ContextualOpenWaterAdmin)

admin.site.register(SeaWeed, SeaWeedAdmin)
admin.site.register(SeaGrass, SeaGrassAdmin)
admin.site.register(Coral, CoralAdmin)
admin.site.register(Sediment, SedimentAdmin)
admin.site.register(Sponge, SpongeAdmin)

