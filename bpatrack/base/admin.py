# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
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
        CommonDataSetAdmin,
        )

from .models import (
        SampleReceived,
        Amplicon,
        Metagenomic,
        TransferLog,
        DataSet,
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


class SampleReceivedResource(resources.ModelResource):
    extraction_id = fields.Field(attribute='extraction_id', column_name='Sample extraction ID')
    batch_number = fields.Field(attribute='batch_number', column_name='Batch number')
    metadata_filename = fields.Field('metadata_filename', column_name='Metadata Filename')
    date_received = DateField(attribute='date_received', column_name='Date received')

    submitter = fields.Field(
            attribute='submitter',
            column_name='Submitter Name',
            widget=UserWidget()
            )

    facility= fields.Field(
            attribute='facility',
            column_name='Facility',
            widget=FacilityWidget()
            )

    class Meta:
        model = SampleReceived
        import_id_fields = ('extraction_id', )
        export_order = (
                'extraction_id',
                'facility',
                'batch_number',
                'date_received',
                'submitter',
                'metadata_filename',
                )

class SampleReceivedAdmin(ImportExportModelAdmin):
    resource_class = SampleReceivedResource
    list_display = (
            'extraction_id',
            'facility',
            'batch_number',
            'date_received',
            'submitter_link',
            )

    date_hierarchy = 'date_received'

    list_filter = (
            'facility',
            'date_received',
            'submitter'
            )

    search_fields = (
            'extraction_id',
            'facility__name',
            'submitter__name',
            'date_received',
            'batch_number'
            )

    def submitter_link(self, obj):
        name = obj.submitter.username
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("users:detail", kwargs={'username': name}),
            name)
            )
    submitter_link.short_description = 'submitter'

admin.site.register(DataSet, CommonDataSetAdmin)
admin.site.register(SampleReceived, SampleReceivedAdmin)
admin.site.register(Amplicon, AmpliconAdmin)
admin.site.register(Metagenomic, MetagenomicAdmin)
admin.site.register(TransferLog, TransferLogAdmin)
