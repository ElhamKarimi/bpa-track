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

class ContextualPelagicAdmin(ImportExportModelAdmin):
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


admin.site.register(Amplicon, AmpliconAdmin)
admin.site.register(Metagenomic, MetagenomicAdmin)
admin.site.register(TransferLog, TransferLogAdmin)
admin.site.register(SampleStateTrack, SampleStateTrackAdmin)
admin.site.register(ContextualPelagic, ContextualPelagicAdmin)

